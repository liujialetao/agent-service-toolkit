"""
Streamlit 亲子入门小课堂 🌈
适合家长和孩子一起边玩边学。

运行方式（在项目根目录）：
    streamlit run learn/streamlit_kids_app.py
"""

import random

import streamlit as st

# ---------- 页面设置（每个 Streamlit 程序通常从这里开始）----------
st.set_page_config(
    page_title="小小程序员乐园刘佳的儿子",
    page_icon="🎈",
    layout="centered",
)

# ---------- 初始化 session_state（记住游戏里的数据）----------
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_a" not in st.session_state:
    st.session_state.quiz_a = random.randint(1, 9)
if "quiz_b" not in st.session_state:
    st.session_state.quiz_b = random.randint(1, 9)
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 10)
if "guess_count" not in st.session_state:
    st.session_state.guess_count = 0

# ---------- 侧边栏：给家长看的 Streamlit 小笔记 ----------
with st.sidebar:
    st.header("📚 给家长的小笔记")
    st.markdown(
        """
**Streamlit 是什么？**  
用 Python 写网页的小工具，改代码 → 保存 → 浏览器自动刷新。

**本页用到的组件：**
| 组件 | 作用 |
|------|------|
| `st.title` | 大标题 |
| `st.text_input` | 输入文字 |
| `st.button` | 按钮 |
| `st.slider` | 滑块 |
| `st.selectbox` | 下拉选择 |
| `st.color_picker` | 选颜色 |
| `session_state` | 记住分数、题目等 |

**和孩子一起：** 每玩一个游戏，可以指着对应组件说「这就是 Python 里的 xxx」。
        """
    )
    st.divider()
    st.caption("提示：按 R 键可以刷新页面哦！")

# ---------- 主标题 ----------
st.title("🎈 小小程序员乐园刘佳的儿子")
st.subheader("和爸爸妈妈一起，认识 Streamlit！")

name = st.text_input("👋 你叫什么名字？", placeholder="比如：小明")
if name:
    st.success(f"你好呀，**{name}**！欢迎来玩～")

st.divider()

# ---------- 用 tabs 分成几个小游戏 ----------
tab1, tab2, tab3, tab4 = st.tabs(["🎨 魔法颜色", "➕ 口算挑战", "🐱 动物朋友", "🔢 猜数字"])

# ----- Tab 1: 魔法颜色 -----
with tab1:
    st.markdown("### 拖动滑块，看看颜色怎么变！")
    st.caption("这里用了 `st.slider` 和 `st.color_picker`")

    red = st.slider("红色 🔴", 0, 255, 255)
    green = st.slider("绿色 🟢", 0, 255, 128)
    blue = st.slider("蓝色 🔵", 0, 255, 64)

    hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    st.markdown(
        f'<div style="background-color:{hex_color}; '
        f'height:120px;border-radius:16px;border:3px solid #333;"></div>',
        unsafe_allow_html=True,
    )
    st.write(f"你调出的颜色代码是：`{hex_color}`")

    fav_color = st.color_picker("或者点这里直接选颜色 🎨", "#FFD700")
    st.markdown(
        f'<p style="font-size:28px;color:{fav_color};">'
        f"{'★ ' * 5} 好漂亮！ {'★ ' * 5}</p>",
        unsafe_allow_html=True,
    )

    if st.button("🎉 庆祝一下！", key="balloons"):
        st.balloons()
        st.toast("太棒啦！")

# ----- Tab 2: 口算挑战 -----
with tab2:
    st.markdown("### 口算小挑战（10 以内加法）")
    st.caption("这里用了 `st.number_input` 和 `session_state` 记住题目")

    a, b = st.session_state.quiz_a, st.session_state.quiz_b
    st.markdown(f"## {a}  +  {b}  =  ?")

    answer = st.number_input("你的答案", min_value=0, max_value=20, value=0, step=1)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ 提交答案", key="submit_quiz"):
            if answer == a + b:
                st.session_state.score += 1
                st.success("答对啦！🎊")
                st.balloons()
            else:
                st.error(f"再想想～ 正确答案是 {a + b}")
            st.session_state.quiz_a = random.randint(1, 9)
            st.session_state.quiz_b = random.randint(1, 9)
            st.rerun()

    with col2:
        if st.button("🔄 换一题", key="new_quiz"):
            st.session_state.quiz_a = random.randint(1, 9)
            st.session_state.quiz_b = random.randint(1, 9)
            st.rerun()

    st.metric("🏆 累计得分", st.session_state.score)

# ----- Tab 3: 动物朋友 -----
with tab3:
    st.markdown("### 认识小动物")
    st.caption("这里用了 `st.selectbox` 和 `st.columns`")

    animals = {
        "🐱 小猫": "小猫喜欢睡觉，一天能睡 16 个小时！",
        "🐶 小狗": "小狗的鼻子超厉害，闻气味比人类强很多倍！",
        "🐼 熊猫": "熊猫最爱吃竹子，一天要吃好多好多！",
        "🦁 狮子": "狮子是群居动物，吼声能传很远很远！",
        "🐸 青蛙": "青蛙小时候是蝌蚪，在水里游来游去～",
        "🦋 蝴蝶": "蝴蝶是从毛毛虫变来的，这叫「变态发育」！",
    }

    choice = st.selectbox("选一只小动物", list(animals.keys()))
    st.info(animals[choice])

    mood = st.radio("今天心情怎么样？", ["😊 开心", "🤔 好奇", "😴 想睡觉", "🥳 超兴奋"])
    st.write(f"{name or '小朋友'} 现在 {mood}！")

# ----- Tab 4: 猜数字 -----
with tab4:
    st.markdown("### 猜数字（1 到 10）")
    st.caption("这里用了条件判断 `if / elif / else`")

    guess = st.slider("我猜是……", 1, 10, 5, key="guess_slider")

    if st.button("🔍 猜！", key="guess_btn"):
        st.session_state.guess_count += 1
        secret = st.session_state.secret_number
        if guess < secret:
            st.warning("太小了，再大一点！⬆️")
        elif guess > secret:
            st.warning("太大了，再小一点！⬇️")
        else:
            st.success(f"猜中了！就是 **{secret}**！🎉")
            st.balloons()
            st.session_state.secret_number = random.randint(1, 10)
            # st.session_state.guess_count = 1000

    st.caption(f"你已经猜了 {st.session_state.guess_count} 次")
    st.caption(f"你已经猜了 {st.session_state.guess_count} 次")
    if st.button("🔄 重新开始", key="reset_guess"):
        st.session_state.secret_number = random.randint(1, 10)
        st.session_state.guess_count = 0
        st.rerun()
# ---------- 页脚 ----------
st.divider()
st.markdown(
    "💡 **和爸爸妈妈一起试试：** 打开 `learn/streamlit_kids_app.py`，"
    "改一改上面的文字或数字，保存后看看页面有什么变化！"
)
