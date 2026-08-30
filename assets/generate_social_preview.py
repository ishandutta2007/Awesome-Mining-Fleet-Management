"""
Generate an animated GIF social preview for Awesome-Mining-Fleet-Management.
640x320px with radar sweep, pulsing nodes, animated beam lines, floating truck.
"""
import math
import struct
import zlib
import os

WIDTH, HEIGHT = 640, 320
TOTAL_FRAMES = 60
FRAME_DURATION_MS = 80  # ~12.5 fps

# Color palette
BG_DARK = (9, 13, 22)
BG_MID = (15, 23, 42)
GRID_LINE = (30, 41, 59)
GRID_DOT = (51, 65, 85)
GOLD = (251, 191, 36)
GOLD_DIM = (245, 158, 11)
GOLD_DARK = (180, 83, 9)
CYAN = (6, 182, 212)
CYAN_LIGHT = (56, 189, 248)
GREEN = (16, 185, 129)
GREEN_LIGHT = (52, 211, 153)
PURPLE = (168, 85, 247)
PURPLE_LIGHT = (192, 132, 252)
WHITE = (255, 255, 255)
LIGHT_GRAY = (148, 163, 184)
DARK_GRAY = (71, 85, 105)
TRUCK_BODY = (245, 158, 11)
TRUCK_CANOPY = (217, 119, 6)
WHEEL_RIM = (203, 213, 225)
WHEEL_DARK = (30, 41, 59)


class GIFWriter:
    """Minimal GIF89a writer for animated GIFs with global color table."""

    def __init__(self, filename, width, height, loop=0):
        self.f = open(filename, 'wb')
        self.width = width
        self.height = height
        self.frames = []
        self.loop = loop

    def _write_header(self, global_palette):
        # GIF89a header
        self.f.write(b'GIF89a')
        # Logical screen descriptor
        palette_size = len(global_palette) // 3
        color_bits = max(1, math.ceil(math.log2(palette_size))) if palette_size > 1 else 1
        packed = 0x80 | ((color_bits - 1) << 4) | (color_bits - 1)  # GCT flag, color res, size
        self.f.write(struct.pack('<HH', self.width, self.height))
        self.f.write(struct.pack('B', packed))
        self.f.write(struct.pack('B', 0))  # bg color index
        self.f.write(struct.pack('B', 0))  # pixel aspect ratio
        # Global color table - pad to power of 2
        table_entries = 2 ** color_bits
        padded = global_palette + bytes([0] * (table_entries * 3 - len(global_palette)))
        self.f.write(padded)
        # Netscape extension for looping
        self.f.write(b'\x21\xFF\x0BNETSCAPE2.0\x03\x01')
        self.f.write(struct.pack('<H', self.loop))
        self.f.write(b'\x00')

    def _lzw_compress(self, data, min_code_size):
        clear_code = 1 << min_code_size
        eoi_code = clear_code + 1

        # Simple LZW compression
        result_bits = []
        code_size = min_code_size + 1
        next_code = eoi_code + 1
        max_code = (1 << code_size)

        # Initialize table
        table = {}
        for i in range(clear_code):
            table[(i,)] = i

        def emit(code, nbits):
            for bit in range(nbits):
                result_bits.append((code >> bit) & 1)

        emit(clear_code, code_size)
        buffer = ()

        for byte in data:
            buffer_plus = buffer + (byte,)
            if buffer_plus in table:
                buffer = buffer_plus
            else:
                emit(table[buffer], code_size)
                if next_code < 4096:
                    table[buffer_plus] = next_code
                    next_code += 1
                    if next_code > max_code and code_size < 12:
                        code_size += 1
                        max_code = 1 << code_size
                else:
                    emit(clear_code, code_size)
                    table = {}
                    for i in range(clear_code):
                        table[(i,)] = i
                    code_size = min_code_size + 1
                    next_code = eoi_code + 1
                    max_code = 1 << code_size
                buffer = (byte,)

        if buffer:
            emit(table[buffer], code_size)
        emit(eoi_code, code_size)

        # Pack bits into bytes
        out = bytearray()
        for i in range(0, len(result_bits), 8):
            byte = 0
            for j in range(min(8, len(result_bits) - i)):
                byte |= result_bits[i + j] << j
            out.append(byte)

        return bytes(out)

    def add_frame(self, pixels, palette, delay_ms=100):
        """pixels: list of palette indices, palette: bytes of RGB triples"""
        self.frames.append((pixels, palette, delay_ms))

    def save(self):
        if not self.frames:
            return
        # Use the first frame's palette as global
        global_palette = self.frames[0][1]
        self._write_header(global_palette)

        for pixels, palette, delay_ms in self.frames:
            delay = delay_ms // 10
            # Graphic control extension
            self.f.write(b'\x21\xF9\x04')
            self.f.write(struct.pack('B', 0x00))  # no transparency
            self.f.write(struct.pack('<H', delay))
            self.f.write(struct.pack('B', 0))  # transparent color
            self.f.write(b'\x00')

            # Image descriptor
            self.f.write(b'\x2C')
            self.f.write(struct.pack('<HH', 0, 0))
            self.f.write(struct.pack('<HH', self.width, self.height))
            self.f.write(struct.pack('B', 0x00))  # no local color table

            # Image data
            palette_count = len(global_palette) // 3
            min_code_size = max(2, math.ceil(math.log2(palette_count)) if palette_count > 1 else 2)
            self.f.write(struct.pack('B', min_code_size))

            compressed = self._lzw_compress(pixels, min_code_size)
            # Write in sub-blocks of 255
            pos = 0
            while pos < len(compressed):
                chunk = compressed[pos:pos + 255]
                self.f.write(struct.pack('B', len(chunk)))
                self.f.write(chunk)
                pos += 255
            self.f.write(b'\x00')  # block terminator

        self.f.write(b'\x3B')  # GIF trailer
        self.f.close()


class FrameBuffer:
    """Simple 640x320 framebuffer with RGB pixels and palette quantization."""

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.pixels = [BG_DARK] * (width * height)

    def set_pixel(self, x, y, color):
        ix, iy = int(x), int(y)
        if 0 <= ix < self.w and 0 <= iy < self.h:
            self.pixels[iy * self.w + ix] = color

    def fill(self, color):
        self.pixels = [color] * (self.w * self.h)

    def draw_rect(self, x, y, w, h, color):
        for dy in range(max(0, int(y)), min(self.h, int(y + h))):
            for dx in range(max(0, int(x)), min(self.w, int(x + w))):
                self.pixels[dy * self.w + dx] = color

    def draw_rect_outline(self, x, y, w, h, color, thickness=1):
        for t in range(thickness):
            for dx in range(int(x) - t, int(x + w) + t):
                if 0 <= dx < self.w:
                    if 0 <= int(y) - t < self.h:
                        self.pixels[(int(y) - t) * self.w + dx] = color
                    if 0 <= int(y + h - 1) + t < self.h:
                        self.pixels[(int(y + h - 1) + t) * self.w + dx] = color
            for dy in range(int(y) - t, int(y + h) + t):
                if 0 <= dy < self.h:
                    if 0 <= int(x) - t < self.w:
                        self.pixels[dy * self.w + int(x) - t] = color
                    if 0 <= int(x + w - 1) + t < self.w:
                        self.pixels[dy * self.w + int(x + w - 1) + t] = color

    def draw_circle(self, cx, cy, r, color):
        r2 = r * r
        for dy in range(max(0, int(cy - r - 1)), min(self.h, int(cy + r + 2))):
            for dx in range(max(0, int(cx - r - 1)), min(self.w, int(cx + r + 2))):
                dist2 = (dx - cx) ** 2 + (dy - cy) ** 2
                if dist2 <= r2:
                    self.pixels[dy * self.w + dx] = color

    def draw_circle_outline(self, cx, cy, r, color, thickness=1):
        for dy in range(max(0, int(cy - r - thickness)), min(self.h, int(cy + r + thickness + 1))):
            for dx in range(max(0, int(cx - r - thickness)), min(self.w, int(cx + r + thickness + 1))):
                dist = math.sqrt((dx - cx) ** 2 + (dy - cy) ** 2)
                if abs(dist - r) <= thickness / 2:
                    self.pixels[dy * self.w + dx] = color

    def draw_ellipse_outline(self, cx, cy, rx, ry, color, thickness=1):
        for dy in range(max(0, int(cy - ry - thickness)), min(self.h, int(cy + ry + thickness + 1))):
            for dx in range(max(0, int(cx - rx - thickness)), min(self.w, int(cx + rx + thickness + 1))):
                val = ((dx - cx) / rx) ** 2 + ((dy - cy) / ry) ** 2
                if abs(val - 1.0) < thickness / min(rx, ry):
                    self.pixels[dy * self.w + dx] = color

    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        dx = x1 - x0
        dy = y1 - y0
        length = max(1, int(math.sqrt(dx * dx + dy * dy)))
        for i in range(length + 1):
            t = i / length
            px = x0 + dx * t
            py = y0 + dy * t
            for w in range(-(thickness // 2), (thickness + 1) // 2):
                self.set_pixel(px + w, py, color)
                self.set_pixel(px, py + w, color)

    def draw_line_dashed(self, x0, y0, x1, y1, color, thickness=1, dash_len=6, gap_len=4):
        dx = x1 - x0
        dy = y1 - y0
        length = max(1, int(math.sqrt(dx * dx + dy * dy)))
        cycle = dash_len + gap_len
        for i in range(length + 1):
            if (i % cycle) >= dash_len:
                continue
            t = i / length
            px = x0 + dx * t
            py = y0 + dy * t
            for w in range(-(thickness // 2), (thickness + 1) // 2):
                self.set_pixel(px + w, py, color)
                self.set_pixel(px, py + w, color)

    def draw_line_animated(self, x0, y0, x1, y1, color, progress, thickness=2, trail_len=0.25):
        """Draw a line with an animated pulse that travels along it."""
        dx = x1 - x0
        dy = y1 - y0
        length = max(1, int(math.sqrt(dx * dx + dy * dy)))
        for i in range(length + 1):
            t = i / length
            dist_from_pulse = abs(t - progress)
            if dist_from_pulse > trail_len:
                continue
            alpha = 1.0 - (dist_from_pulse / trail_len)
            blended = blend_color(BG_MID, color, alpha * 0.9)
            px = x0 + dx * t
            py = y0 + dy * t
            for w in range(-(thickness // 2), (thickness + 1) // 2):
                self.set_pixel(px + w, py, blended)
                self.set_pixel(px, py + w, blended)

    def draw_text_simple(self, x, y, text, color, scale=1):
        """Draw text using a minimal 5x7 bitmap font."""
        cx = int(x)
        for ch in text:
            glyph = FONT.get(ch, FONT.get('?', []))
            for row_idx, row in enumerate(glyph):
                for col in range(5):
                    if row & (1 << (4 - col)):
                        for sy in range(scale):
                            for sx in range(scale):
                                self.set_pixel(cx + col * scale + sx, y + row_idx * scale + sy, color)
            cx += 6 * scale

    def quantize(self, max_colors=256):
        """Reduce to palette. Returns (indices, palette_bytes)."""
        # Collect unique colors, keeping a mapping
        color_set = {}
        for c in self.pixels:
            if c not in color_set and len(color_set) < max_colors:
                color_set[c] = len(color_set)

        # If too many colors, do a simple median-cut-like reduction
        if len(set(self.pixels)) > max_colors:
            # Simple approach: map to nearest in palette
            palette_list = list(color_set.keys())
        else:
            palette_list = list(color_set.keys())

        # Build palette bytes
        palette_bytes = bytearray()
        for r, g, b in palette_list:
            palette_bytes.extend([r, g, b])

        # Pad to power of 2
        while len(palette_list) < max_colors:
            palette_bytes.extend([0, 0, 0])
            palette_list.append((0, 0, 0))

        # Map pixels to indices
        indices = []
        for c in self.pixels:
            if c in color_set:
                indices.append(color_set[c])
            else:
                # Find nearest color
                best_idx = 0
                best_dist = float('inf')
                for idx, pc in enumerate(palette_list[:len(color_set)]):
                    d = (c[0] - pc[0]) ** 2 + (c[1] - pc[1]) ** 2 + (c[2] - pc[2]) ** 2
                    if d < best_dist:
                        best_dist = d
                        best_idx = idx
                indices.append(best_idx)

        return indices, bytes(palette_bytes)


def blend_color(c1, c2, alpha):
    """Blend c2 over c1 with alpha [0,1]."""
    return (
        int(c1[0] * (1 - alpha) + c2[0] * alpha),
        int(c1[1] * (1 - alpha) + c2[1] * alpha),
        int(c1[2] * (1 - alpha) + c2[2] * alpha),
    )


# Minimal 5x7 bitmap font for uppercase + digits + punctuation
FONT = {
    'A': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    'C': [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    'D': [0b11100, 0b10010, 0b10001, 0b10001, 0b10001, 0b10010, 0b11100],
    'E': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    'G': [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111],
    'H': [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'J': [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    'K': [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    'N': [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    'S': [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    'X': [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    'Y': [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    '0': [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    '2': [0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
    '3': [0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b10001, 0b01110],
    '4': [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    '6': [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    '8': [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    '9': [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],
    ' ': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    '.': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100],
    ',': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00100, 0b01000],
    '-': [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    '&': [0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101],
    '/': [0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000],
    '(': [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ')': [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    ':': [0b00000, 0b01100, 0b01100, 0b00000, 0b01100, 0b01100, 0b00000],
    '?': [0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0b00000, 0b00100],
}

# Scaled positions for 640x320 (original was 1200x320, scale x by 640/1200 ≈ 0.533)
SX = 640 / 1200

# Haul route waypoints (scaled)
PIT_CENTER = (int(1030 * SX), 160)
SHOVEL1 = (int(680 * SX), 240)
SHOVEL2 = (int(860 * SX), 110)
WP1 = (int(780 * SX), 180)
WP2 = (int(980 * SX), 140)
DUMP = (int(970 * SX), 240)

# Route paths
ROUTE1 = [SHOVEL1, WP1, (int(890 * SX), 200), WP2, PIT_CENTER]
ROUTE2 = [WP1, SHOVEL2, (int(960 * SX), 100), PIT_CENTER]
ROUTE3 = [(int(890 * SX), 200), DUMP, (int(1070 * SX), 210), PIT_CENTER]


def draw_frame(frame_idx):
    fb = FrameBuffer(WIDTH, HEIGHT)
    t = frame_idx / TOTAL_FRAMES  # 0..1 progress through animation cycle

    # 1) Background gradient (approximate with horizontal bands)
    for y in range(HEIGHT):
        fy = y / HEIGHT
        r = int(9 + (15 - 9) * fy * 0.5)
        g = int(13 + (23 - 13) * fy * 0.5)
        b = int(22 + (42 - 22) * fy * 0.5)
        for x in range(WIDTH):
            fb.pixels[y * WIDTH + x] = (r, g, b)

    # 2) Grid overlay
    for y in range(0, HEIGHT, 20):
        for x in range(WIDTH):
            if y < HEIGHT:
                fb.set_pixel(x, y, GRID_LINE)
    for x in range(0, WIDTH, 20):
        for y in range(HEIGHT):
            fb.set_pixel(x, y, GRID_LINE)
    for y in range(0, HEIGHT, 20):
        for x in range(0, WIDTH, 20):
            fb.draw_circle(x, y, 1, GRID_DOT)

    # 3) Topographic pit contours
    pcx, pcy = PIT_CENTER
    fb.draw_ellipse_outline(pcx, pcy, int(140 * SX), 110, blend_color(BG_MID, GOLD_DIM, 0.25))
    fb.draw_ellipse_outline(pcx, pcy, int(105 * SX), 80, blend_color(BG_MID, GOLD_DIM, 0.2))
    fb.draw_ellipse_outline(pcx, pcy, int(70 * SX), 50, blend_color(BG_MID, GOLD_DIM, 0.25))
    fb.draw_ellipse_outline(pcx, pcy, int(35 * SX), 25, blend_color(BG_MID, CYAN, 0.25))

    # 4) Static haul road network
    for route in [ROUTE1, ROUTE2, ROUTE3]:
        for i in range(len(route) - 1):
            fb.draw_line(route[i][0], route[i][1], route[i + 1][0], route[i + 1][1], GRID_DOT, 2)

    # 5) Animated beam pulses along routes
    p1 = t
    p2 = (t + 0.33) % 1.0
    p3 = (t + 0.66) % 1.0
    for route, progress, color in [(ROUTE1, p1, GOLD), (ROUTE2, p2, CYAN_LIGHT), (ROUTE3, p3, GREEN_LIGHT)]:
        total_len = 0
        segs = []
        for i in range(len(route) - 1):
            dx = route[i + 1][0] - route[i][0]
            dy = route[i + 1][1] - route[i][1]
            seg_len = math.sqrt(dx * dx + dy * dy)
            segs.append((route[i], route[i + 1], seg_len))
            total_len += seg_len
        target = progress * total_len
        cum = 0
        for (s, e, sl) in segs:
            if cum + sl >= target:
                local_p = (target - cum) / sl
                fb.draw_line_animated(s[0], s[1], e[0], e[1], color, local_p, 2, 0.35)
                break
            cum += sl

    # 6) Radar sweep
    radar_angle = t * 2 * math.pi
    sweep_len = int(100 * SX)
    rx = pcx + math.cos(radar_angle) * sweep_len
    ry = pcy + math.sin(radar_angle) * sweep_len
    # Draw a fading radar arm
    for i in range(max(1, sweep_len)):
        ti = i / sweep_len
        ax = pcx + math.cos(radar_angle) * i
        ay = pcy + math.sin(radar_angle) * i
        alpha = 0.3 * (1 - ti * 0.5)
        c = blend_color(BG_MID, CYAN, alpha)
        fb.set_pixel(ax, ay, c)
        fb.set_pixel(ax + 1, ay, c)
        fb.set_pixel(ax, ay + 1, c)
    # Fading trail behind the arm
    for trail in range(1, 20):
        trail_angle = radar_angle - trail * 0.03
        for i in range(max(1, sweep_len)):
            ti = i / sweep_len
            ax = pcx + math.cos(trail_angle) * i
            ay = pcy + math.sin(trail_angle) * i
            alpha = 0.08 * (1 - trail / 20) * (1 - ti * 0.5)
            c = blend_color(BG_MID, CYAN, alpha)
            fb.set_pixel(ax, ay, c)

    # 7) Waypoint nodes (with pulsing)
    pulse = (math.sin(t * 2 * math.pi) + 1) / 2  # 0..1
    pulse2 = (math.sin(t * 2 * math.pi + 1.5) + 1) / 2
    pulse3 = (math.sin(t * 2 * math.pi + 3.0) + 1) / 2

    # Pit center
    fb.draw_circle(pcx, pcy, 7, BG_MID)
    fb.draw_circle_outline(pcx, pcy, 7, CYAN, 2)
    fb.draw_circle(pcx, pcy, int(3 + 2 * pulse), blend_color(CYAN, CYAN_LIGHT, pulse))

    # Shovels
    for (sx, sy), p in [(SHOVEL1, pulse2), (SHOVEL2, pulse3)]:
        fb.draw_circle(sx, sy, 5, BG_MID)
        fb.draw_circle_outline(sx, sy, 5, GOLD_DIM, 1)
        fb.draw_circle(sx, sy, int(2 + 2 * p), blend_color(GOLD_DIM, GOLD, p))

    # Waypoints
    fb.draw_circle(WP1[0], WP1[1], 4, BG_MID)
    fb.draw_circle_outline(WP1[0], WP1[1], 4, CYAN, 1)
    fb.draw_circle(WP1[0], WP1[1], 2, CYAN_LIGHT)

    fb.draw_circle(WP2[0], WP2[1], 4, BG_MID)
    fb.draw_circle_outline(WP2[0], WP2[1], 4, GREEN, 1)
    fb.draw_circle(WP2[0], WP2[1], 2, GREEN_LIGHT)

    # Dump
    fb.draw_circle(DUMP[0], DUMP[1], 5, BG_MID)
    fb.draw_circle_outline(DUMP[0], DUMP[1], 5, PURPLE, 1)
    fb.draw_circle(DUMP[0], DUMP[1], int(2 + 1.5 * pulse), blend_color(PURPLE, PURPLE_LIGHT, pulse))

    # 8) Floating haul truck (simple 2D silhouette)
    truck_y_offset = math.sin(t * 2 * math.pi) * 3
    tx, ty = int(480 * SX), int(30 + truck_y_offset)
    # Body
    fb.draw_rect(tx, ty + 5, 32, 16, TRUCK_BODY)
    # Canopy
    for dx in range(24):
        h = int(5 * (1 - dx / 24))
        fb.draw_rect(tx + dx, ty + 5 - h, 1, h, TRUCK_CANOPY)
    # Cab window
    fb.draw_rect(tx + 3, ty + 8, 7, 6, BG_DARK)
    # Body ribs
    for rx in [14, 20, 26]:
        fb.draw_line(tx + rx, ty + 6, tx + rx, ty + 19, GOLD_DARK, 1)
    # Wheels
    for wx in [7, 26]:
        fb.draw_circle(tx + wx, ty + 22, 6, WHEEL_DARK)
        fb.draw_circle_outline(tx + wx, ty + 22, 6, DARK_GRAY, 1)
        fb.draw_circle(tx + wx, ty + 22, 2, WHEEL_RIM)

    # 9) Title text
    fb.draw_text_simple(20, 25, "AWESOME MINING", WHITE, 2)
    fb.draw_text_simple(20, 48, "FLEET MANAGEMENT", GOLD, 2)

    # Subtitle
    fb.draw_text_simple(20, 78, "DISPATCH . HAULAGE . TELEMETRY . AHS", LIGHT_GRAY, 1)

    # Description lines
    fb.draw_text_simple(20, 100, "CURATED SAAS PLATFORMS AND", blend_color(BG_MID, LIGHT_GRAY, 0.7), 1)
    fb.draw_text_simple(20, 112, "OPEN SOURCE FLEET TRACKING TOOLS", blend_color(BG_MID, LIGHT_GRAY, 0.7), 1)

    # Feature tags
    tag_y = 140
    tags = [
        ("DISPATCH", GOLD),
        ("TELEMATICS", CYAN_LIGHT),
        ("AHS", GREEN_LIGHT),
        ("VRP", PURPLE_LIGHT),
    ]
    tag_x = 20
    for label, color in tags:
        tw = len(label) * 6 + 8
        fb.draw_rect(tag_x, tag_y, tw, 12, BG_MID)
        fb.draw_rect_outline(tag_x, tag_y, tw, 12, color)
        fb.draw_text_simple(tag_x + 4, tag_y + 3, label, color, 1)
        tag_x += tw + 5

    # Status pill at top
    fb.draw_rect(20, 8, 180, 12, blend_color(BG_MID, GRID_LINE, 0.4))
    status_pulse_color = blend_color(GREEN, GREEN_LIGHT, pulse)
    fb.draw_circle(30, 14, 3, status_pulse_color)
    fb.draw_text_simple(38, 10, "AUTONOMOUS AND DISPATCH FMS", LIGHT_GRAY, 1)

    # Bottom accent lines
    for x in range(15, 180):
        fb.set_pixel(x, HEIGHT - 3, blend_color(GOLD_DIM, GOLD, (x - 15) / 165))
    for x in range(460, 625):
        fb.set_pixel(x, HEIGHT - 3, blend_color(CYAN, CYAN_LIGHT, (x - 460) / 165))

    return fb


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "social_preview.gif")

    print(f"Generating {TOTAL_FRAMES}-frame animated GIF at {WIDTH}x{HEIGHT}...")
    gif = GIFWriter(output_path, WIDTH, HEIGHT, loop=0)

    for i in range(TOTAL_FRAMES):
        print(f"  Rendering frame {i + 1}/{TOTAL_FRAMES}...", end='\r')
        fb = draw_frame(i)
        indices, palette = fb.quantize(256)
        gif.add_frame(indices, palette, FRAME_DURATION_MS)

    gif.save()
    print(f"\nSaved to: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == '__main__':
    main()
