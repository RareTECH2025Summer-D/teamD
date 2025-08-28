from django.views.generic import ListView, DetailView,CreateView,UpdateView,TemplateView,View
from django.contrib.auth.views import LoginView,LogoutView,FormView
from django.db.models import Q, F
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.db import transaction

# ===============================
# サインアップ
# ===============================
class UserSignup(CreateView):
    model = Users
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # フォームが有効な際に実行
        user = form.save(commit=False)                      # 入力フォームの情報を取得
        user.set_password(form.cleaned_data["password"])    # passwordをハッシュ化
        user.save()
        return super().form_valid(form)


# ===============================
# ログイン
# ===============================
class Login(LoginView):
    model = Users
    # LoginViewのテンプレとして、formはclass_formを見ているので、form_classを定義
    form_class = LoginForm
    

    def get_success_url(self):
        user = self.request.user    # ログインした Users モデルのインスタンス
        is_teacher = user.just_before_status
        user_id = user.id

        # UserProfileの確認
        # 条件合致：True　不一致：False
        created_profile = has_profile = UserProfile.objects.filter(
            user_id=user_id,
            is_teacher = is_teacher
        ).exists()

        if created_profile:
            if is_teacher:
                # 先生
                base_url = reverse('user_home')
                return f"{base_url}?role=teacher"
            else:
                # 生徒
                base_url = reverse('user_home')
                return f"{base_url}?role=student"
        else:
            # プロフィール作成
            base_url = reverse('user_home')
            return base_url

# ===============================
# ホーム画面
# ===============================
class UserHome(TemplateView):

    def post(self, request, *args, **kwargs):
        role = request.POST.get("user_role")  # "teacher" or "student"
        user = self.request.user    # ログインした Users モデルのインスタンス
        user_id = user.id

        if role == "teacher":
            is_teacher = True
        else:
            is_teacher= False
        
        
        # UserProfileの確認
        # 条件合致：True　不一致：False
        created_profile = UserProfile.objects.filter(
            user_id=user_id,
            is_teacher = is_teacher
        ).exists()

        if created_profile:
            # Users.just_before_status を更新
            user.just_before_status = is_teacher
            user.save()
            
            if is_teacher:
                # 先生
                base_url = reverse_lazy('user_home')
                return redirect(f"{base_url}?role=teacher")
            else:
                # 生徒
                base_url = reverse_lazy('user_home')
                return redirect(f"{base_url}?role=student")
        else:
            # UserProfile なし → setup_skill にリダイレクト
            base_url = reverse_lazy("setup_skill")
            return redirect(f"{base_url}?role={role}")
            
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Loginviewから受け取るroleを確認　roleがある場合はFalse、ない場合はtrueに分岐
        # セッションの有無はLoginviewで確認しているのでここではGETリクエストの確認でOKでした
        
        role = self.request.GET.get('role') 
        
        if role not in ["student", "teacher"]:
            context["is_opening_home"] = True
            # role = "guest" # 今はguestとしてCSSで制御しているわけではないのでコメントアウト
        else:
            context["is_opening_home"] = False

        context["role"] = role
        return context




# ===============================
# スキル登録画面
# ===============================
def skill_setup_view(request):
    user = Users.objects.get(id=request.user.id)
    role = request.GET.get("role")
    save_flag = request.GET.get("save")

    # セッションから選択済みスキルと作成済みスキルを取得
    selected_skills = request.session.get("selected_skills", [])
    created_skills = request.session.get("created_skills", [])
    
    # 作成済みスキルをDBに保存してID取得
    created_skill_ids = []
    for skill_name in created_skills:
        skill_obj, _ = Skills.objects.get_or_create(skill_name=skill_name)
        created_skill_ids.append(skill_obj.id)

    # 選択済みスキル + 作成済みスキルを統合
    all_selected_ids = list(set(selected_skills + created_skill_ids))
    request.session["selected_skills"] = all_selected_ids
    request.session["created_skill_ids"] = created_skill_ids

    # role に応じたタイトルと just_before_status の設定
    if role == "student":
        user.just_before_status = False
        page_title = "学びたいスキルを<br>選択してください！"
    else:
        user.just_before_status = True
        page_title = "教えたいスキルを<br>選択してください！"
    user.save()
    request.session["just_before_status"] = role

    # ---------------- GET: save=1 の場合 ----------------
    if save_flag == "1":
        # GET の場合でもセッションに保存（作成画面に遷移する前提）
        # 既存のセッション情報をそのまま保持するだけ
        request.session.modified = True
        return redirect(f"{reverse('user_create_skill')}?role={role}")

    # ---------------- POST ----------------
    if request.method == "POST":
        form = SkillSelectForm(request.POST, created_skills_ids=created_skill_ids)
        if form.is_valid():
            # 選択内容をセッションに保存
            request.session["selected_skills"] = list(
                form.cleaned_data["skills"].values_list("id", flat=True)
            )
            request.session.modified = True
            return redirect(f"{reverse('user_setup_profile')}?role={role}")

    # ---------------- GET ----------------
    else:
        # 初期値用 QuerySet（戻ったときにチェックを復元）
        initial_qs = Skills.objects.filter(id__in=all_selected_ids)
        form = SkillSelectForm(
            initial={"skills": initial_qs},
            created_skills_ids=created_skill_ids
        )

    return render(request, 'app/skill_registration.html', {
        "role": role,
        "page_title": page_title,
        "form": form
    })


# ===============================
# スキル作成画面
# ===============================
def skill_create_view(request):
    role = request.GET.get("role", "student")

    if request.method == "POST":
        form = SkillCreationForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data.get('skill_name')
            skills = request.session.get('created_skills', [])
            if skill_name not in skills:
                skills.append(skill_name)
            request.session['created_skills'] = skills
            request.session.modified = True
            return redirect(f"{reverse('setup_skill')}?role={role}")
    else:
        form = SkillCreationForm()

    page_title = "学びたいスキルを<br>追加しましょう！" if role == "student" else "教えたいスキルを<br>追加しましょう！"

    return render(request, 'app/skill_create.html', {
        "role": role,
        "page_title": page_title,
        "form": form
    })


# ===============================
# プロフィール作成画面
# ===============================
def profile_create_view(request):
    user = request.user
    role = request.GET.get("role", "student")
    is_teacher = True if role == 'teacher' else False

    # UserProfile がすでに存在する場合はエラー
    if UserProfile.objects.filter(user_id=user, is_teacher=user.just_before_status).exists():
        messages.error(request, "すでに存在します。")
        return redirect(f"{reverse('user_home')}?role={role}")

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = user
            profile.contact_info = user.email
            profile.is_teacher = is_teacher
            profile.save()

            # UserSkills 保存
            selected_skills = request.session.get("selected_skills", [])
            created_skills = request.session.get("created_skills", [])

            for skill_name in created_skills:
                new_skill, _ = Skills.objects.get_or_create(skill_name=skill_name)
                if new_skill.id not in selected_skills:
                    selected_skills.append(new_skill.id)

            for skill_id in selected_skills:
                skill_obj = Skills.objects.get(id=skill_id)
                UserSkills.objects.create(
                    user_id=user,
                    skill_id=skill_obj,
                    is_teacher=is_teacher
                )
                Skills.objects.filter(id=skill_id).update(skill_count=F("skill_count") + 1)

            # セッション削除
            request.session.pop("selected_skills", None)
            request.session.pop("created_skills", None)
            request.session.modified = True

            return redirect(f"{reverse('user_home')}?role={role}")
    else:
        form = ProfileForm(initial={"contact_info": user.email})

    return render(request, "app/profile_create.html", {
        "form": form,
        "role": role
    })



# プロフィール画面表示
def requester_profile_view(request):
    role = request.GET.get("role", "student")
    
    if role == "student":
        sub_text = "教えたいもの："
    elif role == "teacher":
        sub_text = "学びたいもの："
    
    return render(request, 'app/requester_profile.html', {
        "role": role,
        "sub_text": sub_text
    })



#設定画面
class Setting(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        role = self.request.GET.get("role", "student")


        context["role"] = role

        return context










# プロフィール編集
# class ProfileUpdate(UpdateView):
#     def get():

#         pass

#     def post():
#         pass










# 先生・生徒検索(学ぶ・教える共通)
class SearchUsers(TemplateView):
    template_name = 'app/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 本番用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        # ログイン時にセッションを取得してroleをURLに組み込むのでGETメソッドでOK
        role = self.request.GET.get("role")
        # Matchingsテーブルからログイン中のユーザーがリクエストしたユーザーIDを取得
        is_requested = Matchings.objects.filter(
            requested_user_id=self.request.user.id).values_list('requested_user_id__id', flat=True)
        
        is_request = Matchings.objects.filter(requester_user_id=self.request.user.id).values_list('requested_user_id__id', flat=True)

        if role == "student":
            page_title = "先生を探す"
            login_user =Users.objects.get(id=self.request.user.id)
            login_user_role = login_user.just_before_status #モデルに書き込む必要があるためFalseで取得する
            # ログイン中のroleに紐づくユーザーのスキル一覧を取得 skill_idフィールドのみが欲しいのでvalue_listを使用する
            login_user_skills = UserSkills.objects.filter(
                user_id=self.request.user.id, is_teacher=False).values_list('skill_id', flat=True)
            # userprofilesからrole=teacherでかつログイン中のユーザーが学びたいスキルを登録していユーザーid一覧を取得する
            serch_users = UserProfile.objects.filter(
                user_id__userskills__skill_id__in=login_user_skills,user_id__userskills__is_teacher=True).exclude(user_id__in=is_requested).distinct()
            
                  
        elif role == "teacher":
            page_title = "生徒を探す"
            login_user =Users.objects.get(id=self.request.user.id)
            login_user_role = login_user.just_before_status
            login_user_skills = UserSkills.objects.filter(user_id=self.request.user.id, is_teacher=True).values_list('skill_id', flat=True)
            serch_users = UserProfile.objects.filter(
                user_id__userskills__skill_id__in=login_user_skills,user_id__userskills__is_teacher=False).exclude(user_id__in=is_requested).distinct()
            
        else:
            serch_users = UserProfile.objects.none()

        
        # users=ログイン中のユーザーが持つスキルに合致する場合のUserProfile情報
        # ※usersはexcludeですでにリクエスとした、リクエストされたユーザーを除外している
        # not_maching_listで条件に合致したニックネーム一覧とボタンに表示する文言のcontextを作成する
        
        request_list = []
        
        # requester_status = Matchings.objects.filter(
        #     requester_user_id=self.request.user.id,requested_user_id=serch_users.user_id.id).values_list('requester_status', flat=True)
        
        for user in serch_users:
            if user.user_id.id in is_request:
                request_status = "リクエスト済み"
            else:
                request_status = "リクエストする"
                
            request_list.append({
                "requested_id": user.user_id.id,
                "requeted_nickname": user.nickname,
                "request_status": request_status,
                "requester_role": login_user_role, # True: 先生, False: 生徒
            })


            
        context["role"] = role #GETリクエストで受け取ったrole,teacher or student
        context["page_title"] = page_title
        context["users"] = request_list
        context["excluded_users_ids"] = is_requested 
        context["login_user"] = login_user # ログイン中のユーザーのjust_before_status

        return context

    
    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')
        if form_type == 'send_request':
            try:
                requester_user_id = request.user.id  # リクエストを送信するユーザーのID=ログイン中のユーザー
                # リクエストを受け取るユーザーのID　HTMLのフォームで表示されているユーザーを取得できるようにする
                requested_user_id = request.POST.get('requested_user_id')
                requester_user_role = request.POST.get('requester_user_role')
                get_role = request.POST.get('get_role')
                
                with transaction.atomic():
                    # マッチングの作成
                    Matchings.objects.create(
                        requester_user_id_id = requester_user_id,
                        requested_user_id_id = requested_user_id,
                        requester_user_role = requester_user_role,
                        requester_status = 'リクエスト中',
                        requested_status = '承認する'
                    )
                return redirect(f"{reverse_lazy('search')}?role={get_role}")
            except Exception as e:
                # エラーハンドリング
                print(f"リクエスト中にエラーが発生しました: {e}")
                return redirect(f"{reverse_lazy('user_home')}?role={get_role}")
            
        else:
             return redirect(f"{reverse_lazy('user_home')}?role={get_role}")
        
        
        
        # POSTリクエストの処理
        # ここではリクエストを送信するためのロジックを実装することができます
        # 例えば、リクエストされたユーザーIDを取得し、マッチングを作成するなど
        # リクエストの送信後は、適切なリダイレクトやレスポンスを返すことができます
        
        # 例: リクエストされたユーザーIDを取得
        requested_user_id = request.POST.get('requested_user_id')
        
        # マッチングの作成処理などをここに実装
#         pass










# ユーザー詳細画面(学ぶ・教える共通)


# ユーザー詳細画面(学ぶ・教える共通)
# フロント画面作成用
class UserDetail(TemplateView):
    template_name = 'app/user_profile.html'

    def get_context_data(self,**kwargs):

        user_id = self.request.GET.get("requested_user_id")
        request_status = self.request.GET.get("request_status")
        role = self.request.GET.get("role")

        if role == "teacher":
            is_teacher = False
            requester_user_role = "True"
        else:
            is_teacher = True
            requester_user_role = "False"


        obj = get_object_or_404(UserProfile, user_id=user_id, is_teacher=is_teacher)


        # 自分のロールがteacher
        if role == "teacher":
            skills = list(
                UserSkills.objects
                .filter(user_id=obj.user_id, is_teacher=False)
                .values_list('skill_id__skill_name', flat=True)
            )
        # 自分のロールがstudent
        else:
            skills = list(
                UserSkills.objects
                .filter(user_id=obj.user_id, is_teacher=True)
                .values_list('skill_id__skill_name', flat=True)
            )

        return {
            "requested_user_id" : obj.user_id_id,
            "nickname" : obj.nickname,
            "self_introduction" : obj.self_introduction,
            "role" : role,
            "skills" : skills,
            "request_status" : request_status,
            "requester_user_role" : requester_user_role,
        }










#リクエスト送信(学ぶ・教える共通)
class SendRequest(FormView):
    def get():

        pass

    def post():
        pass










# リクエスト一覧(学ぶ・教える共通)
class RequestList(ListView):
    # Matchingにあとで変えてください（画面表示のため異なるテーブル名で記述）
    model = Matchings
    template_name = 'app/handshake.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.request.GET.get("role")
        # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        context["role"] = role
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.GET.get("role")
        if role == "student":
            # filterで指定した条件に合致するレコードをすべて取得
            request_list = queryset.filter(requester_user_id=self.request.user.id,requester_user_role=True)
            requested_list = queryset.filter(requested_user_id=self.request.user.id,requester_user_role=True)
            full_list = request_list | requested_list
            return full_list
        elif role == "teacher":
            request_list = queryset.filter(requester_user_id=self.request.user.id,requester_user_role=False)
            requested_list = queryset.filter(requested_user_id=self.request.user.id,requester_user_role=False)
            full_list = request_list | requested_list
            return full_list
        else:
            return queryset.none()
        
        
        
        
#     def get():

#         pass

#     def post():
#         pass










# # 承認・削除送信(学ぶ・教える共通)
# class RequestApproval(TemplateView):
#     def get():

#         pass

#     def post():
#         pass










# マッチング成立一覧(学ぶ・教える共通)
# class MatchingList(ListView):
#     def get():

#         pass

#     def post():
#         pass










# コンタクト
class Contact(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        role = self.request.GET.get("role", "student")

        if role == "student":
            sub_text = "教えたいもの："
        elif role == "teacher":
            sub_text = "学びたいもの："

        context["role"] = role
        context["sub_text"] = sub_text

        return context
#     def get():

#         pass

#     def post():
#         pass











# 評価
# class Review(CreateView):
#     def get():

#         pass

#     def post():
#         pass