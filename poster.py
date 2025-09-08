import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import io
import requests

def load_image_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content)).convert("RGBA")
    return img


def draw_multiline_text(draw, text, position, font, max_chars, fill, line_spacing=8):
    """Wrap and draw text neatly inside boxes"""
    wrapped_lines = textwrap.wrap(text, width=max_chars)
    y_offset = position[1]
    for line in wrapped_lines:
        draw.text((position[0], y_offset), line, font=font, fill=fill)
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        y_offset += line_height + line_spacing

def paste_rounded_image(base, img, position, radius=50):
    """Paste an image with rounded mask onto base"""
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    base.paste(img, position, mask)

st.title("Custom Telugu Poster Generator")

canvas_width, canvas_height = 1300, 1800

# Load background or solid color
try:
    bg_image = load_image_from_drive("https://drive.google.com/file/d/1XphcT8WRftLRXsfuMSYanJdHuSqgiaUU/view?usp=sharing")  # replace with your actual file ID
    bg_image = bg_image.resize((canvas_width, canvas_height))
except:
    bg_image = Image.new("RGBA", (canvas_width, canvas_height), (0, 41, 127))

poster = bg_image.copy()
draw = ImageDraw.Draw(poster)

# --- Load and place the 3 top portraits ---
try:
    img_t1 = load_image_from_drive("https://drive.google.com/file/d/13JOrfDblJjAjJIcgHLQk8VWrVoHqTMVh/view?usp=sharing").resize((200, 180))
    img_t2 = load_image_from_drive("https://drive.google.com/file/d/1OBv_HGEwCMocHRez2XyQPLCYU8g1zr3J/view?usp=sharing").resize((200, 180))
    img_t3 = load_image_from_drive("https://drive.google.com/file/d/1tKG4p5xOmK8_E2oThaUzmcqEMy9i7jkq/view?usp=sharing").resize((200, 180))
except:
    img_t1 = Image.new("RGBA", (200, 180), (200, 200, 200, 255))
    img_t2 = Image.new("RGBA", (200, 180), (180, 180, 180, 255))
    img_t3 = Image.new("RGBA", (200, 180), (160, 160, 160, 255))

# Paste portraits neatly spaced
paste_rounded_image(poster, img_t1, (100, 20), radius=90)
paste_rounded_image(poster, img_t2, (525, 20), radius=90)
paste_rounded_image(poster, img_t3, (950, 20), radius=90)

# Fixed texts
fixed_title_text1 = "లీలా గ్రూప్ చైర్మన్ డా,,మోహన్ నాయక్"
fixed_title_text2 = "కాంగ్రెస్ పార్టీ నాయకులు"

# Date input
event_date = st.text_input("Enter Event Date (dd-mm-yyyy):", "04-08-2025")
date_heading = f"గారి తేదీ:{event_date}"
date_subheading = "పర్యటన వివరాలు"

# Load fonts
try:
    font_title = ImageFont.truetype("NotoSansTelugu-Bold.ttf", 72)   # bold & bigger
    font_subtitle = ImageFont.truetype("NotoSansTelugu-Regular.ttf", 44)
    font_date = ImageFont.truetype("NotoSansTelugu-Bold.ttf", 42)
    font_schedule_bold = ImageFont.truetype("NotoSansTelugu-Bold.ttf", 34)
    font_schedule = ImageFont.truetype("NotoSansTelugu-Regular.ttf", 34)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_date = ImageFont.load_default()
    font_schedule_bold = ImageFont.load_default()
    font_schedule = ImageFont.load_default()

# --- White Box (Title Section) ---
white_box_pos = (70, 215, 1250, 370)
draw.rectangle(white_box_pos, fill="white")

# Title
bbox1 = font_title.getbbox(fixed_title_text1)
w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
title_x = (canvas_width - w1) // 2
draw.text((title_x, 220), fixed_title_text1, font=font_title, fill=(145, 62, 6))

# Subtitle
bbox2 = font_subtitle.getbbox(fixed_title_text2)
w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
subtitle_x = (canvas_width - w2) // 2
draw.text((subtitle_x, 210 + h1 + 15), fixed_title_text2, font=font_subtitle, fill=(0, 0, 0))

# --- Green Box (Date Section) ---
date_box_pos = (350, 380, 950, 500)
draw.rectangle(date_box_pos, fill=(0, 100, 0))
draw.rectangle(date_box_pos, outline="white", width=5)

# Date heading
bbox3 = font_date.getbbox(date_heading)
w3, h3 = bbox3[2] - bbox3[0], bbox3[3] - bbox3[1]
date_x1 = (canvas_width - w3) // 2
draw.text((date_x1, 395), date_heading, font=font_date, fill="white")

# Date subheading
bbox4 = font_date.getbbox(date_subheading)
w4, h4 = bbox4[2] - bbox4[0], bbox4[3] - bbox4[1]
date_x2 = (canvas_width - w4) // 2
draw.text((date_x2, 395 + h3 + 10), date_subheading, font=font_date, fill="white")

# --- Schedule Section ---
st.subheader("Enter Schedule Text:")
schedule_text = st.text_area(
    "Write your schedule content here",
    value="""1. 11:00 గంటలకు మేడేక్ మండలం మాచవరం గ్రామంలో అల్లిపురం పోచమ్మ గారు అనారోగ్య కారణంతో మరణించారు వారి కుటుంబాన్ని కలిసి పరామర్శించి ఆర్థిక సహాయాన్ని అందిస్తారు.
2. 12:00 గంటలకు హావెలీ ఫస్నూర్ మండలం చొట్టపల్లి గ్రామంలో చంద్రయ్య గారు ఆర్థిక సమస్యలతో మరణించారు వారి కుటుంబాన్ని కలిసి పరామర్శించి ఆర్థిక సహాయాన్ని అందిస్తారు.
3. 12:15 నిమిషాలకు హావెలీ ఫస్నూర్ మండలం చొట్టపల్లి గ్రామంలో మంద పాశయ్య గారు ఆక్సిడెంట్ లో మరణించారు వారి కుటుంబాన్ని కలిసి పరామర్శించి ఆర్థిక సహాయం అందిస్తారు.
4. 12:30 నిమిషాలకు హావెలీ ఫస్నూర్ మండలం చొట్టపల్లి గ్రామంలో బండమీది సిద్ధయ్య ఉస్మాన్ గారు ఆపరేషన్ అయినదును వారి ని కలిసి పరామర్శిస్తారు."""
)

schedule_lines = [line.strip() for line in schedule_text.split("\n") if line.strip()]

schedule_box_start_y = 550
schedule_box_height = 250
schedule_box_margin = 30

for i, line in enumerate(schedule_lines):
    box_top = schedule_box_start_y + i * (schedule_box_height + schedule_box_margin)
    box_bottom = box_top + schedule_box_height
    box_pos = (90, box_top, 800, box_bottom)
    
    # Light blue background
    draw.rectangle(box_pos, fill="#b5e3ff")
    
    # Split the line to separate the time from the rest of the text
    parts = line.split(' ', 2)
    time_text = parts[0] + " " + parts[1] if len(parts) > 1 else ""
    rest_of_text = parts[2] if len(parts) > 2 else ""

    # Draw the bold time text
    start_x = 100
    start_y = box_top + 15
    draw.text((start_x, start_y), time_text, font=font_schedule_bold, fill=(0, 0, 0))

    # Calculate the starting position for the rest of the text
    time_bbox = font_schedule_bold.getbbox(time_text)
    x_offset = start_x + (time_bbox[2] - time_bbox[0]) + 10 # Add 10 for some space after the bold text

    # Draw the rest of the schedule text with the regular font
    draw_multiline_text(draw, rest_of_text, (x_offset, start_y), font_schedule, max_chars=34, fill=(0, 0, 0))

# Final poster
st.image(poster, caption="Generated Poster", use_container_width=True)

# Download option
buf = io.BytesIO()
poster.save(buf, format="PNG")
byte_im = buf.getvalue()
st.download_button("Download Poster as PNG", data=byte_im, file_name="generated_telugu_poster.png", mime="image/png")

