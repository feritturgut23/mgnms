from Process.Cache.admins import admins
from ImageFont.main import call_py
from datetime import datetime
from asyncio import sleep 
from pyrogram import Client, filters
from Process.decorators import authorized_users_only
from Process.filters import command, other_filters
from Process.queues import QUEUE, clear_queue
from Process.utils import skip_current_song, skip_item
from Config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Geri Git", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 Kapat", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ **Doğru şekilde yeniden yüklendi !**\n✅ **Yönetici listesi güncellendi!**"
    )


@Client.on_message(command(["atla", f"atla@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Menü", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• Kapat", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ şu anda hiçbir şey oynanmıyor")
        elif op == 1:
            await m.reply("✅ __Sıra__ **Boş.**\n\n**• userbot sesli sohbetten ayrıldı**")
        elif op == 2:
            await m.reply("🗑️ **Sıraları Temizleme**\n\n**• userbot sesli sohbeti bıraktı**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **Sonraki parçaya atlatıldı.**\n\n☑️ **İsim:** [{op[0]}]({op[1]})\n💭 **Sohbet:** `{chat_id}`\n💡 **Durum:** `Müzik çalıyor`\n🎧 **Talep eden:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **şarkıyı sıradan kaldırdı:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["son", f"son@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vson"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ Userbot'un görüntülü sohbet bağlantısı kesildi.")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **hiç akış yok**")


@Client.on_message(
    command(["durdur", f"durdur@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **parça duraklatıldı.**\n\n• **Akışı sürdürmek için**\n» /devam komut."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **akışta hiçbir şey yok**")


@Client.on_message(
    command(["devam", f"devam@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **İzleme devam etti.**\n\n• **Akışı duraklatmak için**\n» /durdur komut."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **akışta hiçbir şey yok**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **Userbot sessize alındı.**\n\n• **Kullanıcı robotunun sesini kapatmak için**\n» /unmute komut."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **akışta hiçbir şey yok**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **Userbot'un sesi açıldı.**\n\n• **Kullanıcı robotunun sessizini almak için**\n» /mute komut."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **nothing in streaming**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ the streaming has paused", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ akış yeniden başlatıldı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **Bu akış sona erdi**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 userbot başarıyla sessize alındı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 userbot başarıyla Sessiz", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **birim olarak ayarlandı** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **akışta hiçbir şey yok**")

        
@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "💬 akış duraklatıldı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "💬 akış yeniden başlatıldı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("💬 **Bu akış sona erdi**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"💬 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön .")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu butto'ya dokunabilirn !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "💬 userbot succesfully muted", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "💬 userbot başarıyla Sessiz", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 şu anda hiçbir şey akışa sahip değil", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"💬 **volume set to** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"💬 **error:**\n\n`{e}`")
    else:
        await m.reply("💬 **nothing in streaming**")
      
# Yetki Vermek için (auth) Yetki almak için (unauth) komutlarını ekledim.
# Gayet güzel çalışıyor. @Mahoaga Tarafından Eklenmiştir. 
@Client.on_message(command(["auth", "ver"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        a = await message.reply("Kullanıcıya Yetki Vermek için yanıtlayınız!")
        await sleep(3)
        await a.delete()
        return
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        a = await message.reply("kullanıcı yetkili.")
        await sleep(3)
        await a.delete()
    else:
        e = await message.reply("✅ Kullanıcı Zaten Yetkili!")
        await sleep(3)
        await e.delete()


@Client.on_message(command(["unauth", "al"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        a = await message.reply("✘ Kullanıcıyı yetkisizleştirmek için mesaj atınız!")
        await sleep(3)
        await a.delete()
        return
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        a = await message.reply("kullanıcı yetkisiz")
        await sleep(3)
        await a.delete()
    else:
        e = await message.reply("✔ Kullanıcının yetkisi alındı!")
        await sleep(3)
        await e.delete() 
