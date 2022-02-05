from time import time
from datetime import datetime
from Config import BOT_USERNAME
from Process.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Process.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **Merhabalar {message.from_user.first_name}** \n
🎯 **[Talia Müzik](https://t.me/Sohbetdestek) Telegramın Sesli sohbetinde bana, Müzik çalmam için izin veriniz.**
🔮 **Üzerine tıklayarak komutları çalıştırın ve ögreniniz.**
❓ **Bu botun tüm özellikleri hakkında bilgi almak için, basınız. /help**
🔉 **Sesli sohbetlerde müzik çalmak için, [Talia Resmi Kanal](https://t.me/Sohbetdestek) Tarafından yapılmıştır.**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Beni Grubuna Ekle➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                         "🎯 Developer", url="https://t.me/OrmanCocuklariylaMucadele"
                    ),
                    InlineKeyboardButton(
                        "📣 Resmi Kanal", url=f"https://t.me/Sohbetdestek")
                ],[
                    InlineKeyboardButton(
                        "💬 Group", url=f"https://t.me/BOTDESTEKGRUBU"
                    ),
                    InlineKeyboardButton(
                        "🎶 Mp3 Botu", url=f"https://t.me/Mp3_aramaBot")               
                 ],[
                    InlineKeyboardButton(
                        "🇹🇷 Repo", url="https://github.com/Mehmetbaba55"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✔ **Bot çalışıyor**\n<b>☣ **ᴜᴘᴛɪᴍᴇ:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☢ Group", url=f"https://t.me/BOTDESTEKGRUBU"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal", url=f"https://t.me/SohbetDestek"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>☢ ʜᴇʟʟᴏ {message.from_user.mention()}, ᴘʟᴇᴀsᴇ ᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇssᴀɢᴇ ʏᴏᴜ ᴄᴀɴ ʀᴇᴀᴅ ғᴏʀ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✔ Beni nasıl kullanılırsın", url=f"https://t.me/{BOT_USERNAME}?start=help"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>Merhaba {message.from_user.mention()}, yardım menüsüne hoş geldiniz✨
\n📙 𝙱𝙴𝙽İ 𝙽𝙰𝚂𝙸𝙻 𝙺𝚄𝙻𝙻𝙰𝙽𝙸𝚁𝚂𝙸𝙽?
\n1. Önce beni grubunuza ekleyin.
2. beni yönetici olarak tanıtın ve tüm izinleri verin.
3. Ardından, @Musicbotu_bot grubunuza el ile ekleyiniz.
3. Müzik çalmaya başlamadan önce sesli sohbeti açtığınızdan emin olun.
\n💁🏻‍♀️ **tüm kullanıcı için komutlar:**
\n/oynat - youtube'dan şarkı çalmak
/oynat - ses dosyasını kullanarak şarkı çalma youtube linki veya Mp3 oynatıcı
/vplay - vdeo izlemek için ve video oynatıcı komutu 
/bul - youtube'dan şarkı indirme
/ara - youtube'dan video arama detayı link bulmak
/vbul (video name) - youtube'dan video indirme ayrıntılı 
\n👷🏻‍♂️ **yöneticiler için komutlar:**
/durdur - müzik akışını duraklatma
/devam - devam et müzik duraklatıldı 
/atla - sonraki şarkıya atlamak 
/son - müzik akışını durdurma  
/reload - yönetici listesini yenilemek için 
/auth - müzik botu kullanmak için yetkili kullanıcı 
/unauth - müzik botu kullanmak için yetkisiz 
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☣ Group", url=f"https://t.me/BOTDESTEKGRUBU"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal", url=f"https://t.me/SohbetDestek"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♞🏻‍ Developer 🇹🇷", url=f"https://t.me/Mahoaga"
                    )
                ]
            ]
        )
    )
