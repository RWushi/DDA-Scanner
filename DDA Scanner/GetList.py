from Config import ag_bot

async def get_list():
    output_file = 'Список групп.txt'
    chats = []

    async with ag_bot:
        dialogs = await ag_bot.get_dialogs()

        for dialog in dialogs:
            if dialog.is_group:
                entity = dialog.entity

                if hasattr(entity, 'username') and entity.username:
                    chat_link = f"https://t.me/{entity.username}"
                else:
                    chat_link = f"https://t.me/c/{entity.id}"
                chats.append(chat_link)

        with open(output_file, 'w', encoding='utf-8') as file:
            for chat in chats:
                file.write(f"{chat}\n")

    return output_file, len(chats)
