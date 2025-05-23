import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

def generate_certificates(template_path, excel_path, output_dir, 
                         name_font_size=48, college_font_size=30, 
                         name_position=(535, 480), college_position=(535, 530),
                         name_align="center", college_align="center",
                         name_color=(0, 0, 0), college_color=(0, 0, 0)):
    """
    Generate certificates from a template and attendance data in Excel
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        df = pd.read_excel(excel_path)
        print(f"Loaded {len(df)} records from {excel_path}")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    required_columns = ['Name', 'College']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Excel file is missing required columns: {', '.join(missing_columns)}")
        print(f"Available columns: {', '.join(df.columns)}")
        return

    try:
        template = Image.open(template_path)
        print(f"Loaded template from {template_path}")
    except Exception as e:
        print(f"Error loading template image: {e}")
        return

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
            name_font = college_font = paragraph_font = paragraph_bold = ImageFont.load_default()

    for index, row in df.iterrows():
        name = str(row.get('Name', '')).strip()
        college = str(row.get('College', '')).strip()
        gender = str(row.get('Gender') or '').strip().capitalize()

        if not name or not college:
            print(f"Skipping row {index+2} due to missing name or college")
            continue

        name = name.upper()
        college = college.upper()

        if not name.lower().startswith("dr"):
            if gender == 'Male' and not name.lower().startswith("shri."):
                name = "Shri. " + name
            elif gender == 'Female' and not name.lower().startswith("smt."):
                name = "Smt. " + name

        certificate = template.copy()
        draw = ImageDraw.Draw(certificate)

        name_width = draw.textlength(name, font=name_font)
        college_width = draw.textlength(college, font=college_font)

        name_x = get_aligned_x(name_position[0], name_width, name_align)
        college_x = get_aligned_x(college_position[0], college_width, college_align)

        draw.text((name_x, name_position[1]), name, fill=name_color, font=name_font)
        draw.text((college_x, college_position[1]), college, fill=college_color, font=college_font)

        # Paragraph generation
        paragraph_x = 535  # center
        paragraph_y = college_position[1] + 70

        before_event = f"This Certificate is to certify {name} of {college} has participated in six days online faculty development program on "
        event_name = "“Agentic AI and Large Language Models”"
        after_event = " conducted by the department of Computer Science and Engineering from 03/05/2025 to 09/05/2025."

        full_message = before_event + event_name + after_event
        max_width = certificate.width - 100

        words = full_message.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            width = draw.textlength(test_line, font=paragraph_font)
            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        for line in lines:
            event_index = line.find(event_name)
            line_width = draw.textlength(line, font=paragraph_font)
            line_x = paragraph_x - line_width / 2

            if event_name in line:
                before, after = line.split(event_name)
                bx = line_x
                draw.text((bx, paragraph_y), before, fill=(0, 0, 0), font=paragraph_font)
                bx += draw.textlength(before, font=paragraph_font)
                draw.text((bx, paragraph_y), event_name, fill=(0, 0, 0), font=paragraph_bold)
                bx += draw.textlength(event_name, font=paragraph_bold)
                draw.text((bx, paragraph_y), after, fill=(0, 0, 0), font=paragraph_font)
            else:
                draw.text((line_x, paragraph_y), line, fill=(0, 0, 0), font=paragraph_font)

            paragraph_y += paragraph_font.size + 5

        # Save certificate
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).strip()
        output_path = os.path.join(output_dir, f"certificate_{safe_name}.png")
        certificate.save(output_path)
        print(f"Generated certificate for {name} from {college}")

    print(f"Successfully generated certificates in {output_dir}")

def get_aligned_x(base_x, text_width, alignment):
    if alignment.lower() == "left":
        return base_x
    elif alignment.lower() == "center":
        return base_x - (text_width / 2)
    elif alignment.lower() == "right":
        return base_x - text_width
    else:
        return base_x - (text_width / 2)

def main():
    parser = argparse.ArgumentParser(description='Generate certificates from template and attendance data')
    parser.add_argument('template', help='Path to certificate template image')
    parser.add_argument('excel', help='Path to Excel file with attendance data')
    parser.add_argument('--output', '-o', default='certificates', help='Directory to save generated certificates')

    parser.add_argument('--name-font-size', type=int, default=45, help='Font size for name text')
    parser.add_argument('--college-font-size', type=int, default=30, help='Font size for college text')

    parser.add_argument('--name-x', type=int, default=270, help='X position for name text')
    parser.add_argument('--name-y', type=int, default=690, help='Y position for name text')
    parser.add_argument('--college-x', type=int, default=325, help='X position for college text')
    parser.add_argument('--college-y', type=int, default=772, help='Y position for college text')

    parser.add_argument('--name-align', default='left', choices=['left', 'center', 'right'], help='Alignment for name')
    parser.add_argument('--college-align', default='left', choices=['left', 'center', 'right'], help='Alignment for college')

    parser.add_argument('--name-color', nargs=3, type=int, default=[0, 0, 0], metavar=('R', 'G', 'B'),
                        help='RGB color for name text (0-255)')
    parser.add_argument('--college-color', nargs=3, type=int, default=[0, 0, 0], metavar=('R', 'G', 'B'),
                        help='RGB color for college text (0-255)')

    args = parser.parse_args()

    generate_certificates(
        args.template,
        args.excel,
        args.output,
        name_font_size=args.name_font_size,
        college_font_size=args.college_font_size,
        name_position=(args.name_x, args.name_y),
        college_position=(args.college_x, args.college_y),
        name_align=args.name_align,
        college_align=args.college_align,
        name_color=tuple(args.name_color),
        college_color=tuple(args.college_color)
    )

if __name__ == "__main__":
    main()
