from Caesar import Caesar


text = ('Живите так,1234'
        'Как вас ведет звезда,'
        'Под кущей обновленной сени.'
        'С приветствием,'
        'Вас помнящий всегда'
        'Знакомый ваш'
        'Сергей Есенин.')
cesar = Caesar(len_text=len(text))
encrypted_text, _ = cesar.encrypt_text(text, 5, 'right', 'ru')
a,b,c=cesar.decrypt_text()
print(a)
print(b)
print(c)

# text = ('132Ле щшцчтьо,Ле лып, фшчобчш, щшцчтьо,Фйф и ыьших,Щъткхтстлвтыё ф ыьочо,Лслшхчшлйччш яшнтхт ле щш фшцчйьоТ бьш-ьш ъосфшоЛ хташ къшыйхт цчо.Ле мшлшътхт:'
#         'Чйц щшъй ъйыыьйьёыи,Бьш лйы тсцэбтхйЦши вйхёчйи ртсчё,Бьш лйц щшъй сй нохш щътчтцйьёыи,Й цшу энох —Фйьтьёыи нйхёво, лчтс..')
# cesar = Caesar(len_text=len(text))
# z,x,v = cesar.decrypt_text(text,'left', None, lang='Русский')
# print(z)
# print(x)
# print(v)