from src.plugins.sign import Sign

from .api import *

rdp = on_command("randomPoem", aliases={"对诗"}, priority=5)

@rdp.handle()
async def _(state: T_State, event: Event):
    data = await getRandomPoem()
    content = data[0]
    title = data[1]
    author = data[2]
    contents = content.split("，")
    rdPart = random.randint(0, len(contents) - 1)
    guess = contents[rdPart]
    if guess[-1] in ["？", "！", "。"]:
        guess = guess[0:-1]
    blank = content.replace(guess, "__________")
    state["raw"] = content
    state["author"] = author
    state["title"] = title
    state["answer"] = guess
    question = f"请听题！\n{blank}"
    await rdp.send(question)
    return


@rdp.receive("answer")
async def __(event: Event, state: T_State, answer: Message = Arg()):
    ans = answer.extract_plain_text()
    if ans == state["guess"]:
        Sign.add(str(event.user_id), 50)
        author = state["author"]
        title = state["title"]
        await rdp.finish(f"答对啦！\n这句诗来自 {author} 的《{title}》。\n您获得了50枚金币。")
    else:
        Sign.reduce(str(event.user_id), 70)
        right = state["raw"]
        author = state["author"]
        title = state["title"]
        await rdp.finish(f"唔……答错了！\n这句诗来自 {author} 的《{title}》。\n很可惜，您失去了70枚金币。\n正确答案为：{right}")