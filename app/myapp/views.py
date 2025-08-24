from django.views.generic import ListView, DetailView,CreateView,UpdateView,TemplateView,View
from django.contrib.auth.views import LoginView,LogoutView,FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.db import transaction

# サインアップ
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


# ログイン
class Login(LoginView):
    model = Users
    # LoginViewのテンプレとして、formはclass_formを見ているので、form_classを定義
    form_class = LoginForm
    
    def get_success_url(self):

        # just_befre_statusのセッションを見て判断
        role = self.request.session.get("just_before_status")
        print('■ROLE：',role)
        if role is None:
            return reverse_lazy('user_home')
        elif role == "teacher":
            # ホーム画面作成時user_homeに変更 →　setup_skillからuserhomeに変更
            base_url = reverse_lazy('user_home')
            return f"{base_url}?role=teacher"
        else:
            # ホーム画面作成時user_homeに変更 →　setup_skillからuserhomeに変更
            base_url = reverse_lazy('user_home')
            return f"{base_url}?role=student"
        


# スキル登録画面
def skill_setup_view(request):
    
    # 開発用にURLパラメータでroleを取得
    role = request.GET.get("role")
    #usersにjust_before_statusを登録するためにインスタンスを作成
    user = Users.objects.get(id=request.user.id)
    form = SkillSelectForm()

    if role == "student":
        # GETリクエストroleがstudentのときUsersモデルのjust_before_statusに設定
        user.just_before_status = False
        user.save() # Usersモデル書き込み
        # 新たにust_before_statusセッションを作成 以後セッションで状態を確認できる
        request.session['just_before_status'] = 'student'  
        page_title = "学びたいスキルを<br>選択してください！"
        
    elif role == "teacher":
        user.just_before_status = True
        user.save()
        request.session['just_before_status'] = 'teacher'
        page_title = "教えたいスキルを<br>選択してください！"
    
    return render(request, 'app/skill_registration.html', {
        "role": role,
        "page_title": page_title,
        "form":form
    })

# スキル作成画面
def skill_create_view(request):
    role = request.GET.get("role", "student")

    if role == "student":
        page_title = "学びたいスキルを<br>作りましょう！"
    elif role == "teacher":
        page_title = "教えたいスキルを<br>作りましょう！"

    return render(request, 'app/skill_create.html', {
        "role": role,
        "page_title": page_title
    })

# プロフィール作成画面
def profile_create_view(request):
    # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
    role = request.GET.get("role", "student")
    
    return render(request, 'app/profile_create.html', {
        "role": role,
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













# ホーム画面
class UserHome(TemplateView):
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
    #     role = self.request.GET.get("role", "student")


    #     context["role"] = role

    #     return context
# エラーで画面表示がされないのを回避のためコメントアウト
#     def get():

#         pass

#     def post():
#         pass  









# 学ぶ・教える選択
# class RoleSelect(TemplateView):
#     pass
#     # def get():

#     #     pass

#     # def post():
#     #     pass  











# 初回スキル登録（学ぶ・教える共通）
# View継承時はtemplate_nameでHTMLファイル指定できないので、render()関数でHTMLファイルの指定をする
# class ProfileCreate(View):
#     def get():

#         # return render(request, 'skill_registration.html', context)
#         pass

#     def post():
#         pass  










# スキル作成
# HTMLファイル確認
# class SkillCreate(View):
#     def get():

#         # return render(request, '.html', context)
#         pass

#     def post():
#         pass  










# プロフィール作成(学ぶ・教える共通)
# class ProfileCreate(View):
#     def get():

#         # return render(request, 'profile_create.html', context)
#         pass

#     def post():
#         pass













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

        # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        # ログイン時にセッションを取得してroleをURLに組み込むのでGETメソッドでOK
        role = self.request.GET.get("role")
        is_request = Machings.objects.filter(requester_user_id=self.request.user.id, ).values_list('requester_user_id', flat=True)
        is_requested = Machings.objects.filter(requested_user_id=self.request.user.id).values_list('requested_user_id', flat=True)
        #　リクエストしたユーザー一覧とリクエストされたユーザー一覧をリスト化して除外するユーザーIDをリストで作成
        excluded_users_ids = list(is_request) + list(is_requested)

        if role == "student":
            page_title = "先生を探す"
            # ログイン中のroleに紐づくユーザーのスキル一覧を取得 skill_idフィールドのみが欲しいのでvalue_listを使用する
            user_skills = UserSkills.objects.filter(user_id=self.request.user.id, is_teacher=False).values_list('skill_id', flat=True)
            # role=teacherでかつログイン中のユーザーに合致するユーザーidを取得する⇒.filter(skill_id__in=login_user_skills)はWHERE skill_id IN (LoginUserSkills)のSQL文に相当
            users = UserProfile.objects.filter(user_id__userskills__skill_id__in=user_skills,
    user_id__userskills__is_teacher=True).exclude(user_id__in=excluded_users_ids).distinct()
                  
        elif role == "teacher":
            page_title = "生徒を探す"
            user_skills = UserSkills.objects.filter(user_id=self.request.user.id, is_teacher=True).values_list('skill_id', flat=True)
            users = UserSkills.objects.filter(user_skills__skill_id__in=user_skills, user_skills__is_teacher=False).exclude(user_id__in=excluded_users_ids).distinct()
            
        else:
            users = UserProfile.objects.none()
        
        # users=ログイン中のユーザーが持つスキルに合致する場合のUserProfile情報
        # ※usersはexcludeですでにリクエスとした、リクエストされたユーザーを除外している
        # not_maching_listで条件に合致したニックネーム一覧とボタンに表示する文言のcontextを作成する
        not_maching_list = []
        for user in users:
            not_maching_list.append({
                "nickname": user.nickname,
                "status": "リクエストする"
            })
            
        context["role"] = role
        context["page_title"] = page_title
        context["users"] = not_maching_list

        return context
    
    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')
        if form_type == 'send_request':
            try:
                requester_user_id = request.user.id  # リクエストを送信するユーザーのID=ログイン中のユーザー
                # リクエストを受け取るユーザーのID　HTMLのフォームで表示されているユーザーを取得できるようにする
                requested_user_id = request.POST.get('requested_user_id')
                requester_user_role = request.POST.get('role')
                
                 # ここにデバッグ用のprint文を追加
                print(f"requester_user_id: {requester_user_id}")
                print(f"requested_user_id: {requested_user_id}")
                print(f"requester_user_role: {requester_user_role}")
                
                with transaction.atomic():
                    # マッチングの作成
                    Machings.objects.create(
                        requester_user_id_id = requester_user_id,
                        requested_user_id_id = requested_user_id,
                        requester_user_role = requester_user_role,
                        requester_status = 'リクエスト中',
                        requested_status = '承認する'
                    )
                return redirect(f"{reverse_lazy('search')}?role={requester_user_role}")
            except Exception as e:
                # エラーハンドリング
                print(f"リクエスト中にエラーが発生しました: {e}")
                return redirect(f"{reverse_lazy('user_home')}?role={requester_user_role}")
            
        else:
             return redirect(f"{reverse_lazy('user_home')}?role={requester_user_role}")
            
        
        
        
        # POSTリクエストの処理
        # ここではリクエストを送信するためのロジックを実装することができます
        # 例えば、リクエストされたユーザーIDを取得し、マッチングを作成するなど
        # リクエストの送信後は、適切なリダイレクトやレスポンスを返すことができます
        
        # 例: リクエストされたユーザーIDを取得
        requested_user_id = request.POST.get('requested_user_id')
        
        # マッチングの作成処理などをここに実装
#         pass










# ユーザー詳細画面(学ぶ・教える共通)

#フロント画面作成用
class UserDetail(TemplateView):
    template_name = 'app/user_profile.html'

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

# class UserDitail(DetailView):
#     def get():

#         pass

#     def post():
#         pass










#リクエスト送信(学ぶ・教える共通)
class SendRequest(FormView):
    def get():

        pass

    def post():
        pass










# リクエスト一覧(学ぶ・教える共通)
class RequestList(ListView):
    # Matchingにあとで変えてください（画面表示のため異なるテーブル名で記述）
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
        role = self.request.GET.get("role", "student")


        context["role"] = role

        return context
        
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