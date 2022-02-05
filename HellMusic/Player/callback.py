from Process.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)







@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim Yöneticisiniz !\n\n» yönetici haklarından kullanıcı hesabına geri dön.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **ayarlar** {query.message.chat.title}\n\n⏸ : pause\n▶️ : resume\n🔇 : mute userbot\n🔊 : unmute userbot\n⏹ : end",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 Kapat", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ Şu anda hiçbir şey akışa sahip değil", show_alert=True)

# WHAT'S UP KANGERS......................................................................................................................................................................................


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Yalnızca sesli sohbetleri yönetme iznine sahip yönetici bu düğmeye dokunabilir !", show_alert=True)
    await query.message.delete()
