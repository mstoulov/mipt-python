телеграм-бот, на название функции или класса языка с++ отвечающий названием библиотеки, в которой она лежит

бот работает так - делать запрос в гугл вида 'cpp reference ' + 'ваш текст'
переходит по первой ссылке
пытается найти на странице фразу 'defined in header' - если находит - пишет ответ, иначе - укорачивает ссылку (на cppreference странички с методами класса не содержат информации о том где класс объявлен, но если спустится до странички с классом - такая информация будет)

для запуска бота необходимо запустить код main.py.
имя бота @cpp_lib_bot
