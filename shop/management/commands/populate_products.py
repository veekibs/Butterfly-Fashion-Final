# Import the necessary tools from Django for creating a management command
from django.core.management.base import BaseCommand
# Import all the models needed to interact with
from shop.models import Product, Order, OrderItem 

# Define a new command class that inherits from Django's BaseCommand
class Command(BaseCommand):
    # A help message that will be displayed if you run 'python manage.py populate_products --help'
    help = 'Populates the database with a list of products'

    # The main logic of the command lives in the 'handle' method
    def handle(self, *args, **kwargs):
         # Print a status message to the terminal
        self.stdout.write('Deleting existing data...')

        # Clear out any old data to ensure a clean slate + prevent duplicates
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()

        # Print another status message
        self.stdout.write('Existing data deleted.')

        # A list of dictionaries, where each dictionary represents a new product to be created
        # The keys in each dictionary must EXACTLY match the field names in the Product model
        products_data = [
            # PRETEEN TOPS
            # light pink beaded t-shirt
            {
                "name": "light pink beaded t-shirt",
                "price": 13,
                # This is the plain background shot
                "image_url": "shop/images/clothes/beaded-tee-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/beaded-tee-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # yellow pretezel oversized graphic print t-shirt
            {
                "name": "yellow pretezel oversized graphic print t-shirt",
                "price": 13,
                # This is the plain background shot
                "image_url": "shop/images/clothes/yellow-pretz-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/yellow-pretz-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # light blue oversized cotton disney lilo and stitch t-shirt
            {
                "name": "light blue oversized cotton disney lilo and stitch t-shirt",
                "price": 18,
                # This is the plain background shot
                "image_url": "shop/images/clothes/lilo-stitch-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/lilo-stitch-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False,
                "is_featured": True
            },
            # pink ditsy shirred blouse
            {
                "name": "pink ditsy shirred blouse",
                "price": 14,
                # This is the plain background shot
                "image_url": "shop/images/clothes/ditsy-pink-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/ditsy-pink-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # white oversized olivia rodrigo t-shirt
            {
                "name": "white oversized olivia rodrigo t-shirt",
                "price": 17,
                # This is the plain background shot
                "image_url": "shop/images/clothes/olivia-rodrigo-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/olivia-rodrigo-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": True
            },
            # purple nirvana t-shirt
            {
                "name": "purple nirvana t-shirt",
                "price": 13,
                # This is the plain background shot
                "image_url": "shop/images/clothes/nirvana-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/nirvana-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # blue and ecru stripe long sleeve rugby top
            {
                "name": "blue and ecru stripe long sleeve rugby top",
                "price": 15,
                # This is the plain background shot
                "image_url": "shop/images/clothes/blue-rugby-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/blue-rugby-model.jpg",
                "category": "preteen",
                "sub_category": "tops",
                "is_new_arrival": False
            },

            #-------------------------------------------------------------------------------

            # PRETEENS BOTTOMS
            # black jersey shorts
            {
                "name": "black jersey shorts",
                "price": 8,
                # This is the plain background shot
                "image_url": "shop/images/clothes/black-shorts-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/black-shorts-model.jpg",
                "category": "preteen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },
            # mid blue pull on embroidered barrel jeans 
            {
                "name": "mid blue pull on embroidered barrel jeans",
                "price": 23,
                # This is the plain background shot
                "image_url": "shop/images/clothes/pull-jeans-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/pull-jeans-model.jpg",
                "category": "preteen",
                "sub_category": "bottoms",
                "is_new_arrival": True
            },
            # light blue cotton denim skirt
            {
                "name": "light blue cotton denim skirt",
                "price": 16,
                # This is the plain background shot
                "image_url": "shop/images/clothes/denim-skirt-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/denim-skirt-model.jpg",
                "category": "preteen",
                "sub_category": "bottoms",
                "is_new_arrival": False,
                "is_featured": True
            },
            # blue wide leg joggers
            {
                "name": "blue wide leg joggers",
                "price": 15,
                # This is the plain background shot
                "image_url": "shop/images/clothes/blue-joggers-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/blue-joggers-model.jpg",
                "category": "preteen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },
            # black side stripe wide leg joggers
            {
                "name": "black side stripe wide leg joggers",
                "price": 15,
                # This is the plain background shot
                "image_url": "shop/images/clothes/black-stripe-joggers-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/black-stripe-joggers-model.jpg",
                "category": "preteen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },

            #-------------------------------------------------------------------------------
            
            # PRETEEN DRESSES
            # pink ditsy shirred sleeve dress
            {
                "name": "pink ditsy shirred sleeve dress",
                "price": 18,
                # This is the plain background shot
                "image_url": "shop/images/clothes/pink-dress-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/pink-dress-model.jpg",
                "category": "preteen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },
            # ecru white floral print ruffle dress
            {
                "name": "ecru white floral print ruffle dress",
                "price": 29,
                # This is the plain background shot
                "image_url": "shop/images/clothes/ecru-ruffle-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/ecru-ruffle-model.jpg",
                "category": "preteen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },
            # blue and pink stripe rib racer summer dress
            {
                "name": "blue and pink stripe rib racer summer dress",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/blue-pink-stripe-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/blue-pink-stripe-model.jpg",
                "category": "preteen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },
            # red paisley frill summer dress 
            {
                "name": "red paisley frill summer dress",
                "price": 17,
                # This is the plain background shot
                "image_url": "shop/images/clothes/red-frill-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/red-frill-model.jpg",
                "category": "preteen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },

            #-------------------------------------------------------------------------------
            
            # PRETEEN SETS/CO-ORDS
            # blue slogan cotton t-shirt and short set
            {
                "name": "blue slogan cotton t-shirt and short set",
                "price": 20,
                # This is the plain background shot
                "image_url": "shop/images/clothes/blue-slogan-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/blue-slogan-model.jpg",
                "category": "preteen",
                "sub_category": "sets",
                "is_new_arrival": True
            },
            # animal print shirt and pleated skirt set
            {
                "name": "animal print shirt and pleated skirt set",
                "price": 36,
                # This is the plain background shot
                "image_url": "shop/images/clothes/animal-print-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/animal-print-model.jpg",
                "category": "preteen",
                "sub_category": "sets",
                "is_new_arrival": False,
                "is_featured": True
            },
            
            # ---- TEENS ---------------------
            # TEEN TOPS
            # matcha green open stitch cropped jumper
            {
                "name": "matcha green open stitch cropped jumper",
                "price": 13,
                # This is the plain background shot
                "image_url": "shop/images/clothes/crop-jumper-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/crop-jumper-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": True
            },
            # grey ariana grande oversized t-shirt
            {
                "name": "grey ariana grande oversized t-shirt",
                "price": 14,
                # This is the plain background shot
                "image_url": "shop/images/clothes/ariana-grande-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/ariana-grande-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # brown knitted pullover jumper
            {
                "name": "brown knitted pullover jumper",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/brown-jumper-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/brown-jumper-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # black faux leather biker jacket
            {
                "name": "black faux leather biker jacket",
                "price": 24,
                # This is the plain background shot
                "image_url": "shop/images/clothes/biker-jacket-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/biker-jacket-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": False,
                "is_featured": True
            },
            # burgundy funnel neck windbreaker jacket
            {
                "name": "burgundy funnel neck windbreaker jacket",
                "price": 15,
                # This is the plain background shot
                "image_url": "shop/images/clothes/windbreaker-jacket-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/windbreaker-jacket-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": True
            },
            # beige contrast collar barn jacket
            {
                "name": "beige contrast collar barn jacket",
                "price": 21,
                # This is the plain background shot
                "image_url": "shop/images/clothes/barn-jacket-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/barn-jacket-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            # brown gingham check blouse
            {
                "name": "brown gingham check blouse",
                "price": 11,
                # This is the plain background shot
                "image_url": "shop/images/clothes/brown-blouse-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/brown-blouse-model.jpg",
                "category": "teen",
                "sub_category": "tops",
                "is_new_arrival": False
            },
            
            #-------------------------------------------------------------------------------

            # TEEN BOTTOMS
            # grey wide leg ripped skater jeans
            {
                "name": "grey wide leg ripped skater jeans",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/grey-skater-jeans-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/grey-skater-jeans-model.jpg",
                "category": "teen",
                "sub_category": "bottoms",
                "is_new_arrival": False,
                "is_featured": True
            },
            # brown wide leg graphic joggers
            {
                "name": "brown wide leg graphic joggers",
                "price": 11,
                # This is the plain background shot
                "image_url": "shop/images/clothes/graphic-joggers-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/graphic-joggers-model.jpg",
                "category": "teen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },
            # light blue wide leg jeans
            {
                "name": "light blue wide leg jeans",
                "price": 16,
                # This is the plain background shot
                "image_url": "shop/images/clothes/light-blue-jeans-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/light-blue-jeans-model.jpg",
                "category": "teen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },
            # charcoal pleated pinstripe skirt
            {
                "name": "charcoal pleated pinstripe skirt",
                "price": 13,
                # This is the plain background shot
                "image_url": "shop/images/clothes/emo-skirt-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/emo-skirt-model.jpg",
                "category": "teen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },
            # grey pleated wide leg jeans
            {
                "name": "grey pleated wide leg jeans",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/grey-pleated-jeans-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/grey-pleated-jeans-model.jpg",
                "category": "teen",
                "sub_category": "bottoms",
                "is_new_arrival": False
            },

            #-------------------------------------------------------------------------------

            # TEENS DRESSES
            # white smocked frill-trimmed dress
            {
                "name": "white smocked frill-trimmed dress",
                "price": 15,
                # This is the plain background shot
                "image_url": "shop/images/clothes/white-smock-dress-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/white-smock-dress-model.jpg",
                "category": "teen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },
            # cream crotchet look dress
            {
                "name": "cream crotchet look dress",
                "price": 16,
                # This is the plain background shot
                "image_url": "shop/images/clothes/crotchet-dress-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/crotchet-dress-model.jpg",
                "category": "teen",
                "sub_category": "dresses",
                "is_new_arrival": True
            },
            # cream tennis dress
            {
                "name": "cream tennis dress",
                "price": 21,
                # This is the plain background shot
                "image_url": "shop/images/clothes/tennis-dress-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/tennis-dress-model.jpg",
                "category": "teen",
                "sub_category": "dresses",
                "is_new_arrival": False,
                "is_featured": True
            },
            # white and blue floral smocked strappy dress
            {
                "name": "white and blue floral smocked strappy dress",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/floral-dress-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/floral-dress-model.jpg",
                "category": "teen",
                "sub_category": "dresses",
                "is_new_arrival": False
            },

            #-------------------------------------------------------------------------------

            # TEENS SETS/CO-ORDS
            # black and white stripe shirred blouse and shorts set
            {
                "name": "black and white stripe shirred blouse and shorts set",
                "price": 12,
                # This is the plain background shot
                "image_url": "shop/images/clothes/stripe-set-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/stripe-set-model.jpg",
                "category": "teen",
                "sub_category": "sets",
                "is_new_arrival": False
            },
            # cream two-piece crotchet look set
            {
                "name": "cream two-piece crotchet look set",
                "price": 27,
                # This is the plain background shot
                "image_url": "shop/images/clothes/crotchet-look-plain.jpg", 
                # This is the new field for the model shot
                "model_image_url": "shop/images/clothes/crotchet-look-model.jpg",
                "category": "teen",
                "sub_category": "sets",
                "is_new_arrival": False
            },
        ]

        # Use a set to keep track of names already added to avoid duplicates
        # This is a precaution in case the list above has items with identical names
        unique_names = set()
        unique_products = []

        for product in products_data:
            if product['name'] not in unique_names:
                unique_products.append(product)
                unique_names.add(product['name'])

        self.stdout.write('Populating the database...')

        # Loop through the final, unique list of products
        for product_data in unique_products:
            # The **product_data syntax "unpacks" the dictionary,
            # turning it into keyword arguments for the create method
            # e.g., name="light pink beaded t-shirt", price=13, ...
            Product.objects.create(**product_data)
        
        # Print a final success message to the terminal, styled in green!
        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {len(unique_products)} unique products!'))