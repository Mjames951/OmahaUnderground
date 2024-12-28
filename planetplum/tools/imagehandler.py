from PIL import Image
from io import BytesIO
from django.conf import settings

#RESIZES OR CROPS IMAGE based on function (func)
def CropPicture(OGpicture, type):
    match type:
        case 'pfp':
            newHeight = settings.PFP_WIDTH_HEIGHT
            newWidth = settings.PFP_WIDTH_HEIGHT
            func = 'crop'
        case 'band':
            newHeight = settings.BAND_WIDTH_HEIGHT
            newWidth = settings.BAND_WIDTH_HEIGHT
            func = 'crop'
        case 'show':
            maxEdge = settings.SHOW_MAX_WIDTH_HEIGHT
            func = 'resize'

    print("\nOMG THE IMAGEHANDLER HAS BEEN CALLED\n")
    try: 
        picture = Image.open(OGpicture)
        picture.verify()
        #reopen due to verify pointer at end of file
        picture = Image.open(OGpicture)

        #convert png to RGB
        if picture.mode in ("RGBA", "LA", "P"):
            picture = picture.convert("RGB")

        match func:
            case 'crop':
                #crop then resize the image with antialiazing optimizer (LANCZOS)
                (width, height) = picture.size
                minside = min(width, height)
                picture = picture.crop(((width - minside) // 2,(height - minside) // 2,(width + minside) // 2,(height + minside) // 2))
                picture = picture.resize((newHeight, newWidth), Image.LANCZOS)
            case 'resize':
                (width, height) = picture.size
                maxside = max(width, height)
                difference = maxside - maxEdge
                picture = picture.resize((height-difference, width-difference), Image.LANCZOS)

        #Create a new picture file to be saved as the image
        temp_picture = BytesIO()
        picture.save(temp_picture, format="JPEG", quality=70, optimize=True)
        temp_picture.seek(0)
        original_name, _ = OGpicture.name.lower().split(".")
        picture = f"{original_name}.jpg"

        print("SUCCESSFUL IMAGE")
        return picture, temp_picture          
    except:
        return None, None