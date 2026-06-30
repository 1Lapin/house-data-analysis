# 生成二维码.py
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# 创建二维码
def create_qr(url, output_path, logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # 生成图像
    img = qr.make_image(fill_color="#1a1a2e", back_color="white")
    img = img.convert('RGBA')
    
    # 添加logo（可选）
    if logo_path:
        logo = Image.open(logo_path)
        logo_size = min(img.size) // 4
        logo = logo.resize((logo_size, logo_size))
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo, pos, logo)
    
    # 添加标题
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # 保存
    img.save(output_path, quality=95)
    print(f"✅ 二维码已保存至: {output_path}")
    return img

# 使用示例
if __name__ == "__main__":
    # GitHub Pages URL（全局可访问）
    dashboard_url = "https://1Lapin.github.io/house-data-analysis/house_python.html"
    
    # 输出路径
    output_path = "D:/桌面2.0/数据分析/house_data/house_python_qr.png"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 生成二维码
    create_qr(dashboard_url, output_path)