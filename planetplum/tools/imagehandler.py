from PIL import Image, ImageOps
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile

#(type of model, modelform being passed, 
#   image handler function name (str) for resizing, 
#   modelinstance if replacing/editing)
def addImage(form, func, modelInstance=None):
    Image = form.cleaned_data['image']
    imageName, newImage = CropPicture(Image, func)
    if not imageName or not newImage:
        form.add_error(None, 'The uploaded file is not a valid image')
        return False
    try: #to save the image
        if not modelInstance: modelInstance = form.save(commit=False)
        modelInstance.image.save(imageName, ContentFile(newImage.read()), save=False)
        return modelInstance
    except:
        form.add_error(None, "Unable to save the uploaded file.")
        modelInstance.delete()
        return None

#RESIZES OR CROPS IMAGE based on function (func)
def CropPicture(OGpicture, type):
    match type:
        case 'pfp':
            newHeight = settings.PFP_WIDTH_HEIGHT
            newWidth = settings.PFP_WIDTH_HEIGHT
            func = 'crop'
        case 'square':
            newHeight = settings.BAND_WIDTH_HEIGHT
            newWidth = settings.BAND_WIDTH_HEIGHT
            func = 'crop'
        case 'smaller':
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
                print("YO TIME FOR THE RESIZE")
                (width, height) = picture.size
                print(f"ORIGINAL SIZE: {width}x{height}")
                maxside = max(width, height)
                print(f"maxside: {maxside}")
                divisor = maxside / maxEdge
                print(f"divisor: {divisor}")
                print(f"new calculated size: {width/divisor}x{height/divisor}")
                picture = picture.resize((round(width/divisor), round(height/divisor)), Image.LANCZOS)
                print(f"real size: {picture.size}")

        picture = ImageOps.exif_transpose(picture) #fixes image rotation on iphone images

        #Create a new picture file to be saved as the image
        temp_picture = BytesIO()
        picture.save(temp_picture, format="JPEG", quality=70, optimize=True)
        temp_picture.seek(0)
        original_name, _ = OGpicture.name.lower().split(".")
        original_name=original_name.split("/")[-1]
        picture = f"{original_name}.jpg"
        return picture, temp_picture          
    except:
        return None, None