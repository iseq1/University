import hashlib

from dbpush import DataPusher

with DataPusher('database.db') as changer:

    def authors_teas():
        # Авторские чаи

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Авторские чаи', name='Чай облепиха с апельсином и имбирем', price='299',
                            description='Данный чай можно приготовить в двух вариантах: черный и зеленый.',
                            photo_path='../static/images/coffee-menu/authors-teas/sea-buckthorn-tea-with-orange-and-ginger.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=154, protein=0, fat=0,
                            carbohydrate=38)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=119, protein=0, fat=0,
                            carbohydrate=29)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='Черный/зеленый чай')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа «облепиха апельсин имбирь»')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='мёд')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='горячая вода')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Авторские чаи', name='Чай малина с клюквой и барбарисом', price='299',
                            description='Данный чай можно приготовить в двух вариантах: черный и зеленый.',
                            photo_path='../static/images/coffee-menu/authors-teas/raspberry-tea-with-cranberry-and-barberry.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=148, protein=0, fat=0,
                            carbohydrate=37)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=114, protein=0, fat=0,
                            carbohydrate=28)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='Черный/зеленый чай')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа «малина-клюква-барбарис»')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='мята')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='горячая вода')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Авторские чаи', name='Чай манго с жасмином и каффир-лаймом', price='299',
                            description='Данный чай можно приготовить в двух вариантах: черный и зеленый.',
                            photo_path='../static/images/coffee-menu/authors-teas/mango-tea-with-jasmine-and-kaffir-lime.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=152, protein=0, fat=0,
                            carbohydrate=36)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=117, protein=0, fat=0,
                            carbohydrate=29)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='Черный/зеленый чай')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа «манго-жасмин-кафирский лайм')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='бадьян')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='горячая вода')

        # //================================================||================================================\\

    def favorite_2023():
        # Любимые напитки 2023

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Любимые напитки 2023', name='Мокачино Апельсиновый брауни', price='299',
                            description='Авторский кофейно-молочный напиток с добавлением пасты "Шоколадный торт с апельсином" и украшения из пудры "Брауни-лам".',
                            photo_path='../static/images/coffee-menu/2023best-coffee/mochaccino-orange-brownie.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=248, protein=10, fat=10, carbohydrate=27)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=195, protein=8, fat=8,
                            carbohydrate=21)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа “Шоколадный торт с апельсином”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='паста “Брауни-лайм”')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Любимые напитки 2023', name='Раф Малина кокос', price='299',
                            description='Нежный кофейно-сливочный напиток с добавлением пасты "Малина-кокос" и украшения из пудры "Малина".',
                            photo_path='../static/images/coffee-menu/2023best-coffee/raf-raspberry-coconut.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=297, protein=10, fat=15, carbohydrate=29)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=227, protein=8, fat=11,
                            carbohydrate=22)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа ”малина-кокос”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='паста “малина”')

        # # //================================================||================================================\\
        #
        changer.insert_data(table='menu', type='Любимые напитки 2023', name='Латте Банановое мороженое с соленой карамелью', price='299',
                            description='Мягкий кофейно-сливочный напиток с добавлением пасты "Банановое мороженое с солёной карамелью" и маршмеллоу.',
                            photo_path='../static/images/coffee-menu/2023best-coffee/latte-banana-ice-cream-with-salted-caramel.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=332, protein=10, fat=13,
                            carbohydrate=42)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=262, protein=8, fat=10,
                            carbohydrate=33)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='основа “банановое мороженое с соленой карамелью”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='маршмеллоу')

        # # //================================================||================================================\\
        #
        changer.insert_data(table='menu', type='Любимые напитки 2023',
                            name='Раф Птичье молоко', price='299',
                            description='Авторский кофейно-молочный напиток с добавлением пасты "Птичье молоко" и украшения из пудры "Темный шоколад".',
                            photo_path='../static/images/coffee-menu/2023best-coffee/raf-birds-milk.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=298, protein=10, fat=15,
                            carbohydrate=29)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=228, protein=8, fat=11,
                            carbohydrate=22)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='основа “птичье молоко”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='темный шоколад')

        # # //================================================||================================================\\
        #
        changer.insert_data(table='menu', type='Любимые напитки 2023',
                            name='Капучино Круассан с кленовым сиропом и грецким орехом', price='299',
                            description='Авторский кофейно-молочный напиток с добавлением соуса "Кленово-ореховый круассан" и украшения из пудры "Кориандр".',
                            photo_path='../static/images/coffee-menu/2023best-coffee/cappuccino-croissant-with-maple-syrup-and-walnuts.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=261, protein=9, fat=9,
                            carbohydrate=35)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=203, protein=7, fat=7,
                            carbohydrate=27)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='соус "Кленово-ореховый круассан"')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='пудра "Кориандр"')

    def classic():
        # Классический кофе

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Раф', price='219',
                            description='Для любителей послаще, кофе на основе эспрессо с добавлением ванильного сахара/сиропа, молока и нежных сливок.',
                            photo_path='../static/images/coffee-menu/classic-coffee/raf.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=312, protein=9, fat=19, carbohydrate=29 )
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=243, protein=7, fat=15, carbohydrate=22)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=381, protein=11, fat=24,
                            carbohydrate=36)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='сливки')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='ванильный сахар/сироп (в ассортименте)')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Латте', price='219',
                            description='Латте — самый крупный и молочный кофейный напиток на основе эспрессо. Подходит для тех, кто не любит резкий вкус кофе. В нем много молока и только одна порция эспрессо. Для придания дополнительных вкусовых ощущений пенку латте часто посыпают добавками: корицей, шоколадом или ореховой крошкой',
                            photo_path='../static/images/coffee-menu/classic-coffee/latte.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=166, protein=9, fat=9,
                            carbohydrate=14)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=129, protein=7, fat=7,
                            carbohydrate=11)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=203, protein=11, fat=11,
                            carbohydrate=17)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Капучино', price='219',
                            description='Капучино – самый известный кофейный напиток на основе эспрессо. Он сохраняет баланс: чувствуется вкус эспрессо, но он не доминирует над вкусом молока. Это золотая середина между латте и флэт уайтом и хороший вариант для первого знакомства с кофе.',
                            photo_path='../static/images/coffee-menu/classic-coffee/cappuccino.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=166, protein=9, fat=9,
                            carbohydrate=14)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=129, protein=7, fat=7,
                            carbohydrate=11)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=203, protein=11, fat=11,
                            carbohydrate=17)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Американо', price='179',
                            description='Американо – эспрессо с добавлением горячей воды. Американо не такой плотный, как эспрессо. И в отличие от фильтрованного кофе, у американо нет четких описаний. Это происходит потому, что зерна для эспрессо обжариваются с другой целью.',
                            photo_path='../static/images/coffee-menu/classic-coffee/americano.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=36, protein=4, fat=4,
                            carbohydrate=14)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=18, protein=2, fat=2,
                            carbohydrate=7)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='вода')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Флэт Уайт', price='249',
                            description='Флэт Уайт — молочный напиток на основе эспрессо с самым насыщенным вкусом. Его особенно любят ценители вкуса эспрессо в чашке. Флэт уайт – отличный вариант для тех, кто любит яркий кофейный вкус, но не может пить кофе без молока.',
                            photo_path='../static/images/coffee-menu/classic-coffee/flat-white.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=116, protein=9, fat=9,
                            carbohydrate=14)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=92, protein=5, fat=5,
                            carbohydrate=8)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Горячий шоколад', price='249',
                            description='Согревающий напиток на основе молока и темного шоколада',
                            photo_path='../static/images/coffee-menu/classic-coffee/hot-chocolate.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=504, protein=19, fat=20,
                            carbohydrate=52)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=376, protein=14, fat=15,
                            carbohydrate=38)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=631, protein=23, fat=25,
                            carbohydrate=65)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='тёмный шоколад')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='маршмеллоу')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Какао', price='219',
                            description='Согревающий напиток на основе молока и молочного шоколада. По желанию подаём с корицей/взбитыми сливками/зефиром.',
                            photo_path='../static/images/coffee-menu/classic-coffee/cocoa.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=423, protein=11, fat=23,
                            carbohydrate=51)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=329, protein=9, fat=15,
                            carbohydrate=40)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=517, protein=13, fat=28    ,
                            carbohydrate=62)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молочный шоколад')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='маршмеллоу')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Эспрессо', price='149',
                            description='Насыщенный черный кофе. Является прототипом таких напитков, как Ристретто и Лунго. Эспрессо - ароматный, плотный, округлый и насыщенный с долгим, сладким послевкусием. Во вкусе превосходствует баланс сладости, хорошей кислотности и очень легкой горечи.',
                            photo_path='../static/images/coffee-menu/classic-coffee/espresso.jpg')
        menu_id = changer.cursor.lastrowid

        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=90, protein=3, fat=3,
                            carbohydrate=12)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Айс Латте', price='249',
                            description='Молочный слоеный кофе с добавлением льда.',
                            photo_path='../static/images/coffee-menu/classic-coffee/ice-latte.jpg')
        menu_id = changer.cursor.lastrowid

        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=176, protein=9, fat=9,
                            carbohydrate=21)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=142, protein=7, fat=7,
                            carbohydrate=18)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=240, protein=12, fat=12,
                            carbohydrate=25)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лед')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Айс Раф', price='249',
                            description='Для любителей послаще: кофе на основе эспрессо с добавлением льда, ванильного сахара или сиропа, молока и нежных сливок.',
                            photo_path='../static/images/coffee-menu/classic-coffee/ice-raf.jpg')
        menu_id = changer.cursor.lastrowid

        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=333, protein=9, fat=19,
                            carbohydrate=32)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=209, protein=6, fat=13,
                            carbohydrate=18)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=469, protein=12, fat=26,
                            carbohydrate=47)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='сливки')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='ванильный сахар')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лед')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Айс Капучино', price='249',
                            description='',
                            photo_path='../static/images/coffee-menu/classic-coffee/ice-cappuccino.jpg')
        menu_id = changer.cursor.lastrowid

        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=176, protein=9, fat=19,
                            carbohydrate=15)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=142, protein=6, fat=7,
                            carbohydrate=13)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=240, protein=12, fat=12,
                            carbohydrate=18)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лед')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Классический кофе', name='Айс Какао', price='249',
                            description='',
                            photo_path='../static/images/coffee-menu/classic-coffee/ice-cocoa.jpg')
        menu_id = changer.cursor.lastrowid

        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=562, protein=14, fat=33,
                            carbohydrate=50)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=365, protein=6, fat=22,
                            carbohydrate=33)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=630, protein=15, fat=33,
                            carbohydrate=76)

        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молочный шоколад')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лед')

    def spring_summer_2024():
        # Весна-Лето-2024

        # //================================================||================================================\\

        # changer.insert_data(table='menu', type='Весна-Лето 2024', name='Капучино Банановый бисквит с клубникой', price='379', description='Молочный кофейный напиток на основе соуса из банана, клубники и нежного бисквита. Усыпан пудрой с ароматом клубники.', photo_path='../static/images/coffee-menu/spring-summer-coffee/cappuccino-banana-sponge-cake-with-strawberries.jpg')
        # menu_id = changer.cursor.lastrowid
        # changer.insert_data(table='menu_size_info', menu_id=1, size='L', kcal=299, protein=9, fat=10, carbohydrate=40)
        # changer.insert_data(table='menu_size_info', menu_id=1, size='M', kcal=231, protein=7, fat=8, carbohydrate=31)
        # changer.insert_data(table='menu_size_info', menu_id=1, size='XL', kcal=380, protein=12, fat=13,
        #                     carbohydrate=51)
        # changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        # changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        # changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Бананово-клубничный бисквит”')
        # changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='пудра "Клубника"')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Айс Капучино Банановый бисквит с клубникой',
                            price='359',
                            description='Холодный вариант авторского капучино с бананом, клубникой и нежным бисквитом.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/ice-cappuccino-banana-sponge-cake-with-strawberries.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=226, protein=8, fat=8, carbohydrate=38)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=226, protein=7, fat=8, carbohydrate=30)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=347, protein=11, fat=11,
                            carbohydrate=48)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='соус “Бананово-клубничный бисквит”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Латте Кокосовый пломбир с манго',
                            price='379',
                            description='Авторский латте с нежным вкусом кокосового пломбира с манго. Украшается кокосовой стружкой.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/latte-coconut-mango-ice-cream.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=353, protein=10, fat=14, carbohydrate=44)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=267, protein=7, fat=11, carbohydrate=33)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=454, protein=13, fat=18,
                            carbohydrate=57)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='паста “Кокосовый пломбир с манго”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='стружка кокосовая')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Айс Латте Кокосовый пломбир с манго',
                            price='359',
                            description='Холодный латте со вкусом кокосового пломбира с манго.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/ice-latte-coconut-ice-cream-with-mango.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=276, protein=8, fat=11, carbohydrate=34)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=239, protein=7, fat=10, carbohydrate=28)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=377, protein=11, fat=15,
                            carbohydrate=46)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='паста “Кокосовый пломбир с манго”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Раф Рисовый пудинг с папайей',
                            price='379',
                            description='Сливочный кофе со вкусом рисового пудинга, украшенный пудрой с ароматом папайи.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/raf-rice-pudding-with-papaya.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=363, protein=10, fat=16, carbohydrate=43)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=274, protein=7, fat=12, carbohydrate=32)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=467, protein=13, fat=20,
                            carbohydrate=56)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='паста “Рисовый пудинг с папайей”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='пудра "Папайя"')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Айс Раф Рисовый пудинг с папайей',
                            price='359',
                            description='Холодный десертный кофейный напиток с ярким вкусом рисового пудинга с папайей.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/ice-rough-rice-pudding-with-papaya.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=268, protein=7, fat=12, carbohydrate=32)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=215, protein=6, fat=9, carbohydrate=25)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=392, protein=9, fat=16,
                            carbohydrate=50)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='молоко')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='паста “Рисовый пудинг с папайей”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Лимонад с Арбузом, ананасом и розой',
                            price='319',
                            description='Освежающий тропический лимонад с арбузом, ананасом и розой.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/lemonade-with-watermelon-pineapple-and-Rose.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=125, protein=0, fat=0, carbohydrate=30)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=90, protein=0, fat=0, carbohydrate=22)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=158, protein=0, fat=0,
                            carbohydrate=39)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Ананас арбуз роза”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Кофейный тоник с Арбузом, ананасом и розой',
                            price='359',
                            description='Кофейная версия лимонада с насыщенным вкусом арбузом, ананасом и розой.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/coffee-tonic-with-watermelon-pineapple-and-rose.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=113, protein=0, fat=0, carbohydrate=28)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=79, protein=0, fat=0, carbohydrate=19)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=146, protein=0, fat=0,
                            carbohydrate=36)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Ананас арбуз роза”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Лимонад с Персиком, маракуйей и цветами апельсина',
                            price='319',
                            description='Яркий лимонад на основе соуса из персика, маракуйи и цветов апельсина.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/lemonade-with-peach-passion-fruit-and-orange-blossom.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=125, protein=0, fat=0, carbohydrate=30)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=90, protein=0, fat=0, carbohydrate=22)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=158, protein=0, fat=0,
                            carbohydrate=39)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Персик маракуйя цветы апельсина”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Кофейный тоник с Персиком, маракуйей и цветами апельсина',
                            price='359',
                            description='Бодрящий холодный напиток на основе эспрессо с ярким вкусом персика, маракуйи и цветов апельсина.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/coffee-tonic-with-peach-passion-fruit-and-orange-blossom.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=113, protein=0, fat=0, carbohydrate=28)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=79, protein=0, fat=0, carbohydrate=19)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=146, protein=0, fat=0,
                            carbohydrate=36)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Персик маракуйя цветы апельсина”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Лимонад с Виноградом, алоэ и лавандой',
                            price='319',
                            description='Освежающий авторский лимонад с виноградом, алоэ и лавандой.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/lemonade-with-grapes-aloe-and-lavender.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=125, protein=0, fat=0, carbohydrate=30)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=90, protein=0, fat=0, carbohydrate=22)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=158, protein=0, fat=0,
                            carbohydrate=39)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Виноград алоэ лаванда”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')

        # //================================================||================================================\\

        changer.insert_data(table='menu', type='Весна-Лето 2024', name='Кофейный тоник с Виноградом, алоэ и лавандой',
                            price='359',
                            description='Холодный тонизирующий кофейный напиток на основе эспрессо с виноградом, алоэ и лавандой.',
                            photo_path='../static/images/coffee-menu/spring-summer-coffee/coffee-tonic-with-grapes-aloe-and-lavender.jpg')
        menu_id = changer.cursor.lastrowid
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='L', kcal=113, protein=0, fat=0, carbohydrate=28)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='M', kcal=79, protein=0, fat=0, carbohydrate=19)
        changer.insert_data(table='menu_size_info', menu_id=menu_id, size='XL', kcal=146, protein=0, fat=0,
                            carbohydrate=36)
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='эспрессо')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лимонадная основа')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='соус “Виноград алоэ лаванда”')
        changer.insert_data(table='menu_description_info', menu_id=menu_id,
                            ingredient='глиттер')
        changer.insert_data(table='menu_description_info', menu_id=menu_id, ingredient='лёд')


    changer.insert_data(table='users', username='admin1', role='admin', password=f"{hashlib.sha256('admin1'.encode('utf-8')).hexdigest()}")
    changer.insert_data(table='admin', admin_login='admin1', name='Смирнов Александр Александрович' )
    changer.insert_data(table='users', username='barista1', role='barista', password=f"{hashlib.sha256('barista1'.encode('utf-8')).hexdigest()}")
    changer.insert_data(table='barista', barista_login='barista1', name='Оспенникова Елизавета', work_time=50 )
    changer.insert_data(table='users', username='barista2', role='barista', password=f"{hashlib.sha256('barista2'.encode('utf-8')).hexdigest()}")
    changer.insert_data(table='barista', barista_login='barista2', name='Айрапетов Андрей', work_time=88 )
    changer.insert_data(table='users', username='barista3', role='barista', password=f"{hashlib.sha256('barista3'.encode('utf-8')).hexdigest()}")
    changer.insert_data(table='barista', barista_login='barista3', name='Александр Левин', work_time=132 )

