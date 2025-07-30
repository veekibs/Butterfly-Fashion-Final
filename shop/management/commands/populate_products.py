from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Populates the database with a list of products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing products...')
        Product.objects.all().delete()

        products_data = [
            # Preteen Tops 
            {"name": "floral & slogan graphic drawstring thermal lined hoodie", "price": 12, "image_url": "shop/images/clothes/blue hoodie.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True},
            {"name": "buffalo plaid zip up dual pocket hooded teddy jacket", "price": 20, "image_url": "shop/images/clothes/teddy front.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "letter print striped trim drop shoulder sweatshirt dress", "price": 15, "image_url": "shop/images/clothes/brown.jpg", "category": "preteen", "sub_category": "top"}, # Was dress
            {"name": "panda & heart embroidery drop shoulder teddy jacket", "price": 21, "image_url": "shop/images/clothes/panda jacket.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "japanese letter & figure graphic hoodie dress", "price": 15, "image_url": "shop/images/clothes/anime.jpg", "category": "preteen", "sub_category": "top"}, # Was dress
            {"name": "letter graphic kangaroo pocket drawstring thermal hoodie", "price": 14, "image_url": "shop/images/clothes/cool.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "high neck solid tee", "price": 5, "image_url": "shop/images/clothes/turtleneck.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True},
            {"name": "puff sleeve zip up dress", "price": 12, "image_url": "shop/images/clothes/puff.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True}, # Was dress
            {"name": "striped & floral patched lettuce trim tee", "price": 7, "image_url": "shop/images/clothes/flopo.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True},
            {"name": "plaid & letter graphic drop shoulder shirt", "price": 16, "image_url": "shop/images/clothes/greenplaid.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "colourblock raglan tee", "price": 11, "image_url": "shop/images/clothes/bp.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "turtleneck lantern sleeve sweater", "price": 14, "image_url": "shop/images/clothes/sweater.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "skull & floral print drop shoulder drawstring thermal costume hoodie", "price": 13, "image_url": "shop/images/clothes/shood.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "ditsy floral print frill trim cami top", "price": 11, "image_url": "shop/images/clothes/ditsy.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "2 in 1 graphic printed tee", "price": 7, "image_url": "shop/images/clothes/animegal.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "floral & letter graphic drop shoulder zip up hoodie", "price": 12, "image_url": "shop/images/clothes/ghood.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "mock neck crisscross hem tee", "price": 7, "image_url": "shop/images/clothes/smile.jpg", "category": "preteen", "sub_category": "top"},
            {"name": "butterfly print cami top & zip up hoodie & sweatpants", "price": 26, "image_url": "shop/images/clothes/cami set.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True},
            {"name": "camo print drop shoulder pullover & leggings", "price": 14, "image_url": "shop/images/clothes/army.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True},
            {"name": "v neck ribbed knit dress with belt", "price": 11, "image_url": "shop/images/clothes/dress.jpg", "category": "preteen", "sub_category": "top", "is_new_arrival": True}, # Was dress
            
            # Preteen Bottoms
            {"name": "letter & floral print jeans", "price": 19, "image_url": "shop/images/clothes/flower jeans.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "brown plaid print mini skirt", "price": 5, "image_url": "shop/images/clothes/skirt.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "sun & moon print high waist jeans", "price": 24, "image_url": "shop/images/clothes/jeans.jpg", "category": "preteen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "mock neck letter embroidery top & trousers", "price": 25, "image_url": "shop/images/clothes/brownie.jpg", "category": "preteen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "buckle strap flap pocket cargo pants", "price": 13, "image_url": "shop/images/clothes/cargo.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "butterfly print sweatpants", "price": 9, "image_url": "shop/images/clothes/sweat.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "knot front cargo trousers", "price": 13, "image_url": "shop/images/clothes/poople.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "camo print straight leg jeans", "price": 21, "image_url": "shop/images/clothes/camosplit.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "2pcs contrast tape pleated skirt", "price": 20, "image_url": "shop/images/clothes/yuigoh.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "heart print jeans", "price": 21, "image_url": "shop/images/clothes/heartprintj.jpg", "category": "preteen", "sub_category": "bottom"},
            {"name": "allover heart print flare leg pants", "price": 8, "image_url": "shop/images/clothes/heartflare.jpg", "category": "preteen", "sub_category": "bottom"},

            # Teen Tops
            {"name": "letter patched striped trim cricket sweater vest", "price": 11, "image_url": "shop/images/clothes/vest.jpg", "category": "teen", "sub_category": "top"},
            {"name": "letter graphic contrast collar thermal lined sweatshirt", "price": 17, "image_url": "shop/images/clothes/blokecore.jpg", "category": "teen", "sub_category": "top"},
            {"name": "shawl collar contrast teddy PU leather coat", "price": 40, "image_url": "shop/images/clothes/shawl.jpg", "category": "teen", "sub_category": "top"},
            {"name": "drop shoulder 3D ear teddy hoodie", "price": 11, "image_url": "shop/images/clothes/teddy.jpg", "category": "teen", "sub_category": "top"},
            {"name": "fuzzy trim open front coat", "price": 35, "image_url": "shop/images/clothes/fuzzy.jpg", "category": "teen", "sub_category": "top"},
            {"name": "checkered & heart pattern sweater vest without tee", "price": 10, "image_url": "shop/images/clothes/vestie.jpg", "category": "teen", "sub_category": "top"},
            {"name": "figure graphic drop shoulder zip up drawstring hoodie", "price": 17, "image_url": "shop/images/clothes/hoodie.jpg", "category": "teen", "sub_category": "top", "is_new_arrival": True},
            {"name": "letter graphic contrast collar crop tee", "price": 15, "image_url": "shop/images/clothes/croptee.jpg", "category": "teen", "sub_category": "top", "is_new_arrival": True},
            {"name": "letter graphic drop shoulder tee", "price": 11, "image_url": "shop/images/clothes/tee.jpg", "category": "teen", "sub_category": "top", "is_new_arrival": True},
            {"name": "eyelet embroidery ruffle trim tie backless top", "price": 7, "image_url": "shop/images/clothes/whiteeye.jpg", "category": "teen", "sub_category": "top"},
            {"name": "grunge off shoulder ruched crop tee", "price": 8, "image_url": "shop/images/clothes/grunge.jpg", "category": "teen", "sub_category": "top"},
            {"name": "3pcs solid backless halter top", "price": 15, "image_url": "shop/images/clothes/halter.jpg", "category": "teen", "sub_category": "top"},
            {"name": "scoop neck bell sleeve crop tee", "price": 8, "image_url": "shop/images/clothes/black.jpg", "category": "teen", "sub_category": "top"},

            # Teen Bottoms
            {"name": "bear pattern teddy trousers", "price": 18, "image_url": "shop/images/clothes/lol.jpg", "category": "teen", "sub_category": "bottom"},
            {"name": "floral print straight leg jeans", "price": 15, "image_url": "shop/images/clothes/floral.jpg", "category": "teen", "sub_category": "bottom"},
            {"name": "star print contrast tape side sweatpants", "price": 16, "image_url": "shop/images/clothes/star sweatpants.jpg", "category": "teen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "high waist tie front flap pocket cargo jeans", "price": 25, "image_url": "shop/images/clothes/cjeans.jpg", "category": "teen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "letter patched striped trim bomber jacket & sweatpants", "price": 27, "image_url": "shop/images/clothes/bomber jacket.jpg", "category": "teen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "ripped cut out straight leg jeans", "price": 24, "image_url": "shop/images/clothes/rjeans.jpg", "category": "teen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "solid ribbed knit crop knit top & knit leggings & duster cardigan", "price": 30, "image_url": "shop/images/clothes/justbrown.jpg", "category": "teen", "sub_category": "bottom", "is_new_arrival": True},
            {"name": "high waist split thigh skirt", "price": 9, "image_url": "shop/images/clothes/skirtt.jpg", "category": "teen", "sub_category": "bottom"},
            {"name": "zip back pleated skirt", "price": 11, "image_url": "shop/images/clothes/pskirt.jpg", "category": "teen", "sub_category": "bottom"},
            {"name": "elastic waist wide leg trousers", "price": 12, "image_url": "shop/images/clothes/wideleg.jpg", "category": "teen", "sub_category": "bottom"},
            {"name": "flap pocket side chain detail buckled belted cargo trousers", "price": 17, "image_url": "shop/images/clothes/gothtro.jpg", "category": "teen", "sub_category": "bottom"},
        ]

        # Use a set to keep track of names already added to avoid duplicates
        unique_names = set()
        unique_products = []
        for product in products_data:
            if product['name'] not in unique_names:
                unique_products.append(product)
                unique_names.add(product['name'])

        self.stdout.write('Populating the database...')
        for product_data in unique_products:
            Product.objects.create(**product_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {len(unique_products)} unique products!'))