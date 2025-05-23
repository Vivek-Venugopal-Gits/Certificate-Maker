# Certificate-Maker

A simple and efficient Python-based Certificate Maker that automates the process of generating personalized certificates using templates and participant data.

## 🚀 Features

- Automatically generates certificates for multiple recipients.
- Uses a template image and overlays names or other details.
- Customizable font, position, and design elements.
- Outputs certificates as image files (e.g., PNG or JPG).

## 🖥️ How It Works

The script takes:
- A certificate template image.
- A list of recipient names (typically from a CSV or text file).
- Font settings (type, size, position).
- Then generates certificates with each recipient's name placed accurately on the template.

---

## 📦 Project Structure

CertificateMaker/
│
├── certificates/ # Here the generated certificates in png mode will be saved
├── fonts/ # Store your desired font in .ttf file mode to access and put in the certificate
├── template/ # Template of the certificate
├── .xlsx file/ # The file containing info
├── certificate_generator.py/ # Main script for generating certificate in png 
├── Command.txt /# This txt files contains how to run the program 
├── png_to_pdf.py/ # Main script for converting png files to pdf
└── README.md # You're here!


⚠️ Note: This project is designed with a hard-coded configuration approach. To customize the alignment, font, size, and style of the certificate content, you will need to manually edit the source code.

To change the font type or fallback fonts, update the block in certificate__generator.py under:

<pre> ```python
try:
    name_font = ImageFont.truetype("fonts/Literata-SemiBold.ttf", name_font_size)
    college_font = ImageFont.truetype("fonts/Literata-SemiBold.ttf", college_font_size)
    paragraph_font = ImageFont.truetype("fonts/Literata-Regular.ttf", 24)
    paragraph_bold = ImageFont.truetype("fonts/Literata-SemiBold.ttf", 24)
except:
    try:
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", name_font_size)
        college_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", college_font_size)
        paragraph_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        paragraph_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        print("Warning: Could not load specified fonts, using default")
        name_font = college_font = paragraph_font = paragraph_bold = ImageFont.load_default()```</pre>

To change the position, font size, alignment, or color of the name and college text, update the argparse configuration:
<pre> ```python
parser.add_argument('--name-font-size', type=int, default=45, help='Font size for name text')
parser.add_argument('--college-font-size', type=int, default=30, help='Font size for college text')
parser.add_argument('--name-x', type=int, default=270, help='X position for name text')
parser.add_argument('--name-y', type=int, default=690, help='Y position for name text')
parser.add_argument('--college-x', type=int, default=325, help='X position for college text')
parser.add_argument('--college-y', type=int, default=772, help='Y position for college text')
parser.add_argument('--name-align', default='left', choices=['left', 'center', 'right'], help='Alignment for name')
parser.add_argument('--college-align', default='left', choices=['left', 'center', 'right'], help='Alignment for college')
parser.add_argument('--name-color', nargs=3, type=int, default=[0, 0, 0], metavar=('R', 'G', 'B'), help='RGB color for name text')
parser.add_argument('--college-color', nargs=3, type=int, default=[0, 0, 0], metavar=('R', 'G', 'B'), help='RGB color for college text')```</pre>


Currently, the script must be modified directly to apply visual changes—there is no GUI or interactive interface to adjust these settings.


## Commmands
### To create certificates
 ```bash
            python certificate_generator.py "<template_name>.png" "<excel_name>.xlsx  ```</pre>


           
### To Convert png files to pdf
```bash

           python png_to_pdf.py "<source folder>" "<destination folder>"
