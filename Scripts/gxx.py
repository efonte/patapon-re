# TODO: all

import math
from collections import namedtuple
from enum import Enum
from io import TextIOWrapper
from pathlib import Path
from struct import pack, unpack


class GECommand(Enum):
    GE_NOP = 0
    GE_VADDR = 0x1
    GE_IADDR = 0x2
    GE_PRIM = 0x4
    GE_BEZIER = 0x5
    GE_SPLINE = 0x6
    GE_BOUNDINGBOX = 0x7
    GE_JUMP = 0x8
    GE_BJUMP = 0x9
    GE_CALL = 0xA
    GE_RET = 0xB
    GE_END = 0xC
    GE_SIGNAL = 0xE
    GE_FINISH = 0xF
    GE_BASE = 0x10
    GE_VERTEXTYPE = 0x12
    GE_OFFSETADDR = 0x13
    GE_ORIGIN = 0x14
    GE_REGION1 = 0x15
    GE_REGION2 = 0x16
    GE_LIGHTINGENABLE = 0x17
    GE_LIGHTENABLE0 = 0x18
    GE_LIGHTENABLE1 = 0x19
    GE_LIGHTENABLE2 = 0x1A
    GE_LIGHTENABLE3 = 0x1B
    GE_DEPTHCLAMPENABLE = 0x1C
    GE_CULLFACEENABLE = 0x1D
    GE_TEXTUREMAPENABLE = 0x1E
    GE_FOGENABLE = 0x1F
    GE_DITHERENABLE = 0x20
    GE_ALPHABLENDENABLE = 0x21
    GE_ALPHATESTENABLE = 0x22
    GE_ZTESTENABLE = 0x23
    GE_STENCILTESTENABLE = 0x24
    GE_ANTIALIASENABLE = 0x25
    GE_PATCHCULLENABLE = 0x26
    GE_COLORTESTENABLE = 0x27
    GE_LOGICOPENABLE = 0x28
    GE_BONEMATRIXNUMBER = 0x2A
    GE_BONEMATRIXDATA = 0x2B
    GE_MORPHWEIGHT0 = 0x2C
    GE_MORPHWEIGHT1 = 0x2D
    GE_MORPHWEIGHT2 = 0x2E
    GE_MORPHWEIGHT3 = 0x2F
    GE_MORPHWEIGHT4 = 0x30
    GE_MORPHWEIGHT5 = 0x31
    GE_MORPHWEIGHT6 = 0x32
    GE_MORPHWEIGHT7 = 0x33
    GE_PATCHDIVISION = 0x36
    GE_PATCHPRIMITIVE = 0x37
    GE_PATCHFACING = 0x38
    GE_WORLDMATRIXNUMBER = 0x3A
    GE_WORLDMATRIXDATA = 0x3B
    GE_VIEWMATRIXNUMBER = 0x3C
    GE_VIEWMATRIXDATA = 0x3D
    GE_PROJMATRIXNUMBER = 0x3E
    GE_PROJMATRIXDATA = 0x3F
    GE_TGENMATRIXNUMBER = 0x40
    GE_TGENMATRIXDATA = 0x41
    GE_VIEWPORTXSCALE = 0x42
    GE_VIEWPORTYSCALE = 0x43
    GE_VIEWPORTZSCALE = 0x44
    GE_VIEWPORTXCENTER = 0x45
    GE_VIEWPORTYCENTER = 0x46
    GE_VIEWPORTZCENTER = 0x47
    GE_TEXSCALEU = 0x48
    GE_TEXSCALEV = 0x49
    GE_TEXOFFSETU = 0x4A
    GE_TEXOFFSETV = 0x4B
    GE_OFFSETX = 0x4C
    GE_OFFSETY = 0x4D
    GE_SHADEMODE = 0x50  # flat or gouraud
    GE_REVERSENORMAL = 0x51
    GE_MATERIALUPDATE = 0x53
    GE_MATERIALEMISSIVE = 0x54  # not sure about these but this makes sense
    GE_MATERIALAMBIENT = 0x55  # gotta try enabling lighting and check :)
    GE_MATERIALDIFFUSE = 0x56
    GE_MATERIALSPECULAR = 0x57
    GE_MATERIALALPHA = 0x58
    GE_MATERIALSPECULARCOEF = 0x5B
    GE_AMBIENTCOLOR = 0x5C
    GE_AMBIENTALPHA = 0x5D
    GE_LIGHTMODE = 0x5E
    GE_LIGHTTYPE0 = 0x5F
    GE_LIGHTTYPE1 = 0x60
    GE_LIGHTTYPE2 = 0x61
    GE_LIGHTTYPE3 = 0x62
    GE_LX0 = 0x63
    # GE_LY0
    # GE_LZ0
    # GE_LX1
    # GE_LY1
    # GE_LZ1
    # GE_LX2
    # GE_LY2
    # GE_LZ2
    # GE_LX3
    # GE_LY3
    # GE_LZ3
    GE_LDX0 = 0x6F
    # GE_LDY0
    # GE_LDZ0
    # GE_LDX1
    # GE_LDY1
    # GE_LDZ1
    # GE_LDX2
    # GE_LDY2
    # GE_LDZ2
    # GE_LDX3
    # GE_LDY3
    # GE_LDZ3
    GE_LKA0 = 0x7B
    # GE_LKB0
    # GE_LKC0
    # GE_LKA1
    # GE_LKB1
    # GE_LKC1
    # GE_LKA2
    # GE_LKB2
    # GE_LKC2
    # GE_LKA3
    # GE_LKB3
    # GE_LKC3
    GE_LKS0 = 0x87
    # GE_LKS1
    # GE_LKS2
    # GE_LKS3
    GE_LKO0 = 0x8B
    # GE_LKO1
    # GE_LKO2
    # GE_LKO3
    GE_LAC0 = 0x8F
    # GE_LDC0
    # GE_LSC0
    # GE_LAC1
    # GE_LDC1
    # GE_LSC1
    # GE_LAC2
    # GE_LDC2
    # GE_LSC2
    # GE_LAC3
    # GE_LDC3
    # GE_LSC3
    GE_CULL = 0x9B
    GE_FRAMEBUFPTR = 0x9C
    GE_FRAMEBUFWIDTH = 0x9D
    GE_ZBUFPTR = 0x9E
    GE_ZBUFWIDTH = 0x9F
    GE_TEXADDR0 = 0xA0
    # GE_TEXADDR1
    # GE_TEXADDR2
    # GE_TEXADDR3
    # GE_TEXADDR4
    # GE_TEXADDR5
    # GE_TEXADDR6
    # GE_TEXADDR7
    GE_TEXBUFWIDTH0 = 0xA8
    # GE_TEXBUFWIDTH1
    # GE_TEXBUFWIDTH2
    # GE_TEXBUFWIDTH3
    # GE_TEXBUFWIDTH4
    # GE_TEXBUFWIDTH5
    # GE_TEXBUFWIDTH6
    # GE_TEXBUFWIDTH7
    GE_CLUTADDR = 0xB0
    GE_CLUTADDRUPPER = 0xB1
    # GE_TRANSFERSRC
    # GE_TRANSFERSRCW
    # GE_TRANSFERDST
    # GE_TRANSFERDSTW
    GE_TEXSIZE0 = 0xB8
    # GE_TEXSIZE1
    # GE_TEXSIZE2
    # GE_TEXSIZE3
    # GE_TEXSIZE4
    # GE_TEXSIZE5
    # GE_TEXSIZE6
    # GE_TEXSIZE7
    GE_TEXMAPMODE = 0xC0
    GE_TEXSHADELS = 0xC1
    GE_TEXMODE = 0xC2
    GE_TEXFORMAT = 0xC3
    GE_LOADCLUT = 0xC4
    GE_CLUTFORMAT = 0xC5
    GE_TEXFILTER = 0xC6
    GE_TEXWRAP = 0xC7
    GE_TEXLEVEL = 0xC8
    GE_TEXFUNC = 0xC9
    GE_TEXENVCOLOR = 0xCA
    GE_TEXFLUSH = 0xCB
    GE_TEXSYNC = 0xCC
    GE_FOG1 = 0xCD
    GE_FOG2 = 0xCE
    GE_FOGCOLOR = 0xCF
    GE_TEXLODSLOPE = 0xD0
    GE_FRAMEBUFPIXFORMAT = 0xD2
    GE_CLEARMODE = 0xD3
    GE_SCISSOR1 = 0xD4
    GE_SCISSOR2 = 0xD5
    GE_MINZ = 0xD6
    GE_MAXZ = 0xD7
    GE_COLORTEST = 0xD8
    GE_COLORREF = 0xD9
    GE_COLORTESTMASK = 0xDA
    GE_ALPHATEST = 0xDB
    GE_STENCILTEST = 0xDC
    GE_STENCILOP = 0xDD
    GE_ZTEST = 0xDE
    GE_BLENDMODE = 0xDF
    GE_BLENDFIXEDA = 0xE0
    GE_BLENDFIXEDB = 0xE1
    GE_DITH0 = 0xE2
    # GE_DITH1
    # GE_DITH2
    # GE_DITH3
    GE_LOGICOP = 0xE6
    GE_ZWRITEDISABLE = 0xE7
    GE_MASKRGB = 0xE8
    GE_MASKALPHA = 0xE9
    GE_TRANSFERSTART = 0xEA
    GE_TRANSFERSRCPOS = 0xEB
    GE_TRANSFERDSTPOS = 0xEC
    GE_TRANSFERSIZE = 0xEE
    GE_VSCX = 0xF0
    GE_VSCY = 0xF1
    GE_VSCZ = 0xF2
    GE_VTCS = 0xF3
    GE_VTCT = 0xF4
    GE_VTCQ = 0xF5
    GE_VCV = 0xF6
    GE_VAP = 0xF7
    GE_VFC = 0xF8
    GE_VSCV = 0xF9
    GE_UNKNOWN_03 = 0x03
    GE_UNKNOWN_0D = 0x0D
    GE_UNKNOWN_11 = 0x11
    GE_UNKNOWN_29 = 0x29
    GE_UNKNOWN_34 = 0x34
    GE_UNKNOWN_35 = 0x35
    GE_UNKNOWN_39 = 0x39
    GE_UNKNOWN_4E = 0x4E
    GE_UNKNOWN_4F = 0x4F
    GE_UNKNOWN_52 = 0x52
    GE_UNKNOWN_59 = 0x59
    GE_UNKNOWN_5A = 0x5A
    GE_UNKNOWN_B6 = 0xB6
    GE_UNKNOWN_B7 = 0xB7
    GE_UNKNOWN_D1 = 0xD1
    GE_UNKNOWN_ED = 0xED
    GE_UNKNOWN_EF = 0xEF
    GE_UNKNOWN_FA = 0xFA
    GE_UNKNOWN_FB = 0xFB
    GE_UNKNOWN_FC = 0xFC
    GE_UNKNOWN_FD = 0xFD
    GE_UNKNOWN_FE = 0xFE
    GE_NOP_FF = 0xFF


GE_VTYPE_TRANSFORM = 0 << 23
GE_VTYPE_THROUGH = 1 << 23
GE_VTYPE_THROUGH_MASK = 1 << 23

GE_VTYPE_TC_NONE = 0 << 0
GE_VTYPE_TC_8BIT = 1 << 0
GE_VTYPE_TC_16BIT = 2 << 0
GE_VTYPE_TC_ = 3 << 0
GE_VTYPE_TC_MASK = 3 << 0
GE_VTYPE_TC_SHIFT = 0

GE_VTYPE_COL_NONE = 0 << 2
GE_VTYPE_COL_565 = 4 << 2
GE_VTYPE_COL_5551 = 5 << 2
GE_VTYPE_COL_4444 = 6 << 2
GE_VTYPE_COL_8888 = 7 << 2
GE_VTYPE_COL_MASK = 7 << 2
GE_VTYPE_COL_SHIFT = 2

GE_VTYPE_NRM_NONE = 0 << 5
GE_VTYPE_NRM_8BIT = 1 << 5
GE_VTYPE_NRM_16BIT = 2 << 5
GE_VTYPE_NRM_ = 3 << 5
GE_VTYPE_NRM_MASK = 3 << 5
GE_VTYPE_NRM_SHIFT = 5

# GE_VTYPE_POSITION_NONE = (0<<5)
GE_VTYPE_POS_8BIT = 1 << 7
GE_VTYPE_POS_16BIT = 2 << 7
GE_VTYPE_POS_ = 3 << 7
GE_VTYPE_POS_MASK = 3 << 7
GE_VTYPE_POS_SHIFT = 7

GE_VTYPE_WEIGHT_NONE = 0 << 9
GE_VTYPE_WEIGHT_8BIT = 1 << 9
GE_VTYPE_WEIGHT_16BIT = 2 << 9
GE_VTYPE_WEIGHT_ = 3 << 9
GE_VTYPE_WEIGHT_MASK = 3 << 9
GE_VTYPE_WEIGHT_SHIFT = 9

GE_VTYPE_weight_count_MASK = 7 << 14
GE_VTYPE_weight_count_SHIFT = 14

GE_VTYPE_morph_count_MASK = 7 << 18
GE_VTYPE_morph_count_SHIFT = 18

GE_VTYPE_IDX_NONE = 0 << 11
GE_VTYPE_IDX_8BIT = 1 << 11
GE_VTYPE_IDX_16BIT = 2 << 11
GE_VTYPE_IDX_32BIT = 3 << 11
GE_VTYPE_IDX_MASK = 3 << 11
GE_VTYPE_IDX_SHIFT = 11

GE_CLEARMODE_COLOR = 1 << 8
GE_CLEARMODE_ALPHA = 1 << 9  # or stencil?
GE_CLEARMODE_Z = 1 << 10
GE_CLEARMODE_ALL = GE_CLEARMODE_COLOR | GE_CLEARMODE_ALPHA | GE_CLEARMODE_Z


def read_bytes(infile: TextIOWrapper, num: int, offset: int = None) -> int:
    if offset:
        infile.seek(offset)
    return infile.read(num)


def read_u8(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("B", read_bytes(infile, 1, offset))[0]


def read_i8(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("b", read_bytes(infile, 1, offset))[0]


def read_u16(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("H", read_bytes(infile, 2, offset))[0]


def read_i16(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("h", read_bytes(infile, 2, offset))[0]


def read_u32(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("I", read_bytes(infile, 4, offset))[0]


def read_i32(infile: TextIOWrapper, offset: int = None) -> int:
    return unpack("i", read_bytes(infile, 4, offset))[0]


def read_f32(infile: TextIOWrapper, offset: int = None) -> float:
    return unpack("f", read_bytes(infile, 4, offset))[0]


def read_f64(infile: TextIOWrapper, offset: int = None) -> float:
    return unpack("d", read_bytes(infile, 4, offset))[0]


def read_strz(infile: TextIOWrapper, offset: int = None) -> str:
    if offset:
        infile.seek(offset)
    string_bytes = bytearray()
    while (b := read_u8(infile)) != 0x00:
        string_bytes.append(b)
    infile.seek(infile.tell() - 1)
    return string_bytes.decode("utf-8")


def u32_to_f32(u32: int) -> float:
    return unpack("f", pack("I", u32))[0]


def rad2deg(angle: float) -> float:
    # return math.cos(math.radians(angle))
    return angle * 180.0 / math.pi


# def bgr_to_rgba(bgr565: int) -> int:
#     # TODO
#     # https://stackoverflow.com/questions/2442576/how-does-one-convert-16-bit-rgb565-to-24-bit-rgb888
#     # bgr_to_rgba by Owocek
#     # bgr565
#     print("-")
#     print(f"{bgr565:X}")
#     r = (bgr565 << 11 & 0xFFFF) >> 11
#     g = (bgr565 << 5 & 0xFFFF) >> 10
#     b = bgr565 >> 11
#     print("-")
#     print(f"{r=:X}")
#     print(f"{g=:X}")
#     print(f"{b=:X}")
#     r1 = (bgr565 & 0xF800) >> 11
#     g1 = (bgr565 & 0x07E0) >> 5
#     b1 = bgr565 & 0x001F
#     print(f"{r1=:X}")
#     print(f"{g1=:X}")
#     print(f"{b1=:X}")
#     print(f"{r1<<5=:X}")
#     print(f"{g1<<2=:X}")
#     print(f"{b1<<3=:X}")

#     # rgb888
#     r8 = (r * 527 + 23) >> 6
#     g8 = (g * 259 + 33) >> 6
#     b8 = (b * 527 + 23) >> 6
#     print("-")
#     print(f"{r8=:X}")
#     print(f"{g8=:X}")
#     print(f"{b8=:X}")
#     print(f"{((r8) << 24) + ((g8) << 16) + ((b8) << 8) + 0xFF:X}")
#     exit()

#     return ((r8) << 24) + ((g8) << 16) + ((b8) << 8) + 0xFF


Point = namedtuple("Point", "x y z")


class Bone:
    bounding_box = []
    parent_bone_name = ""
    translate = []
    name = ""
    index = 0

    def __str__(self) -> str:
        return f"""\tBone "icon" {{
\t\tBoundingBox {self.bounding_box}
\t\tParentBone "{self.parent_bone_name}"
\t\tTranslate {self.translate}
\t\tDrawPart "{self.name}"
\t\tBoneState Z_SORT {self.index}
\t}}"""


class Motion:
    frameloop = 0
    frames = 0
    framerate = 0

    def __str__(self) -> str:
        return f"""Motion "59b8ebd4" {{
		FrameLoop {self.frameloop}.000000 {self.frames-1}.000000
		FrameRate {self.framerate:0.6f}
		Animate "Bone::icon" Translate 0 "fcurve-0"
		Animate "Bone::icon" RotateQ 0 "fcurve-0"
		Animate "Bone::icon" Scale2 0 "fcurve-1"
		FCurve "fcurve-0" CONSTANT 4 1 0 {{
			0.000000 0.000000 0.000000 -0.000000 1.000000
		}}
		FCurve "fcurve-1" HERMITE 3 3 0 {{
			0.000000 1.000000 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 0.000000 0.000000
			2.000000 1.096750 -0.000000 0.000000 1.096750 -0.000000 0.000000 1.096750 -0.000000 0.000000
			5.000000 1.000000 -0.000000 0.000000 1.000000 -0.000000 0.000000 1.000000 -0.000000 0.000000
		}}
	}}
"""


class BoneMatrix:
    basisX_x = 0.0  # 0,0
    basisX_y = 0.0  # 0,1
    basisX_z = 0.0  # 0,2

    basisY_x = 0.0  # 1,0
    basisY_y = 0.0  # 1,1
    basisY_z = 0.0  # 1,2

    basisZ_x = 0.0  # 2,0
    basisZ_y = 0.0  # 2,1
    basisZ_z = 0.0  # 2,2

    translation_x = 0.0
    translation_y = 0.0
    translation_z = 0.0

    def get_scale_x(self) -> float:
        return math.sqrt(
            self.basisX_x * self.basisX_x
            + self.basisX_y * self.basisX_y
            + self.basisX_z * self.basisX_z
        )

    def get_scale_y(self) -> float:
        return math.sqrt(
            self.basisY_x * self.basisY_x
            + self.basisY_y * self.basisY_y
            + self.basisY_z * self.basisY_z
        )

    def get_scale_z(self) -> float:
        return math.sqrt(
            self.basisZ_x * self.basisZ_x
            + self.basisZ_y * self.basisZ_y
            + self.basisZ_z * self.basisZ_z
        )

    def get_rotation(self) -> Point:
        rotX_x = self.basisX_x / self.get_scale_x()  # 0,0
        # rotX_y = self.basisX_y / self.get_scale_x()  # 0,1
        # rotX_z = self.basisX_z / self.get_scale_x()  # 0,2

        rotY_x = self.basisY_x / self.get_scale_y()  # 1,0
        rotY_y = self.basisY_y / self.get_scale_y()  # 1,1
        rotY_z = self.basisY_z / self.get_scale_y()  # 1,2

        rotZ_x = self.basisZ_x / self.get_scale_z()  # 2,0
        rotZ_y = self.basisZ_y / self.get_scale_z()  # 2,1
        rotZ_z = self.basisZ_z / self.get_scale_z()  # 2,2

        # setFromRotationMatrix(m, order = this._order, update = true) {
        #  assumes the upper 3x3 of m is a pure rotation matrix (i.e, unscaled)

        m11 = rotX_x
        m12 = rotY_x
        m13 = rotZ_x
        # m21 = rotX_y
        m22 = rotY_y
        m23 = rotZ_y
        # m31 = rotX_z
        m32 = rotY_z
        m33 = rotZ_z

        # XYZ:
        y = math.asin(max(-1.0, min(m13, 1.0)))

        if abs(m13) < 0.9999999:
            x = math.atan2(-m23, m33)
            z = math.atan2(-m12, m11)
        else:
            x = math.atan2(m32, m22)
            z = 0.0

        return Point(x=x, y=y, z=z)


# Based on: https://github.com/WondaOxigen/GXXTool3

file_path = Path("./azt_0440.gxx")
print(f"Reading file: {file_path.name}\n")

gxx = open(file_path, "rb")
# outfile = open("azt_0440_python.txt", "w", encoding="utf-8")

section_c = read_u32(gxx, 0x10)
section_b = read_u32(gxx, 0x28)
section_a = read_u32(gxx, 0x30)

main_offsets = read_u32(gxx, section_c)

# Step 1: Texture name
offset_1 = read_u32(gxx, section_c + 0x08)
offset_2 = read_u32(gxx, offset_1)
offset_3 = read_u32(gxx, offset_2 + 0x04)
texture = read_strz(gxx, offset_3)
print(f"Texture: {texture}\n")

# Step 2: Bones
subsection_offset = read_u32(gxx, section_c + 0x8 + 2 * 0x8)
bone_amount = read_u32(gxx, section_c + 0xC + 2 * 0x8)
print(f"Amount of bones: {bone_amount}")

# We go through each bone offset to get it's name
for i in range(bone_amount):
    # first, we grab the offset to specific bone entry
    entry_offset = subsection_offset + 0x8 * i
    bone_integer = read_u32(gxx, entry_offset)
    bone_name_pointer = read_u32(gxx, entry_offset + 0x4)
    bone_name = read_strz(gxx, bone_name_pointer)
    print(f"Bone {i+1}: {bone_name}, unk_1: {bone_integer}")
    bone = Bone()
    bone.name = bone_name
    bone.index = i

# Step 3: Mesh and Animations
block_pointer = read_u32(gxx, section_c + 0x10)
blocks = read_u32(gxx, section_c + 0x14)
print(f"Blocks start at: 0x{block_pointer:X}, {blocks} blocks\n")


for i in range(blocks):
    gxx.seek(block_pointer + (i * 0x10))
    anim_pointer = read_u32(gxx)
    frames = read_u32(gxx)
    framerate = read_f32(gxx)
    frameloop = read_f32(gxx)

    anim_data = read_u32(gxx, anim_pointer)
    bone_amount = read_u32(gxx, section_c + 0xC + 2 * 0x8)
    anim_data_size = read_u32(gxx, anim_data - 0x40 + 0x8)

    print(
        f"Anim ptr: 0x{anim_pointer:X} Anim data: 0x{anim_data:X}, Frames: {frames} Loop: {f'{frameloop:.6f}'.rstrip('0').rstrip('.')} Framerate: {f'{framerate:.6f}'.rstrip('0').rstrip('.')}"
    )
    # print(f"Anim data size: 0x{anim_data_size:X}\n")

    gpu_offset = anim_data
    buffer = read_u32(gxx, gpu_offset)

    unk_instr: set[int] = set()
    vertex_addr = None
    index_addr = None
    return_addr: list[int] = []

    # VERTEX TYPE
    texcoord_type = "NULL"
    color_type = "NULL"
    position_type = "NULL"

    offsets_values = {}

    j = 0
    while j < int(anim_data_size / 4 * frames):
        # We go over the most crucial GPU instructions for us
        # print(f"0x{gpu_offset:X} > ", end="")
        # incremath.asing gpu_offset before parsing instruction, so it can modifieed by instruction
        gpu_offset += 0x4

        match buffer >> 24:
            case GECommand.GE_NOP.value:
                data = (buffer << 8 & 0xFFFFFFFF) >> 8
                if data != 0:
                    values = f"NOP: data=0x{data:X}"
                else:
                    # values = "NOP"
                    values = ""

            case GECommand.GE_VADDR.value:
                data = (buffer << 8 & 0xFFFFFFFF) >> 8
                if data != 0:
                    vertex_addr = data
                    # values = f"VADDR: 0x{data:X}"
                    values = ""

            case GECommand.GE_IADDR.value:
                data = (buffer << 8 & 0xFFFFFFFF) >> 8
                if data != 0:
                    index_addr = data
                    values = f"IADDR: 0x{data:X}"

            case GECommand.GE_PRIM.value:
                count = buffer & 0xFFFF
                type = (buffer >> 16) & 7

                types = [
                    "POINTS",
                    "LINES",
                    "LINE_STRIP",
                    "TRIANGLES",
                    "TRIANGLE_STRIP",
                    "TRIANGLE_FAN",
                    "RECTANGLES",
                    "CONTINUE_PREVIOUS",
                ]

                # values = f"DRAW PRIM \"{types[type] if type < 7  else 'INVALID'}\" count={count} vaddr=0x{vertex_addr:X}, VERTEX DATA:"
                values = f"DRAW PRIM \"{types[type] if type < 7  else 'INVALID'}\" count={count}"

                block_size = 0x00
                if texcoord_type != "NULL":
                    block_size += 0x08
                if color_type != "NULL":
                    block_size += 0x04
                if position_type != "NULL":
                    block_size += 0x0C

                for i in range(count):
                    vertex_string = "  "
                    offset = vertex_addr + block_size * i
                    gxx.seek(offset)

                    u, v = 0.0, 0.0

                    if texcoord_type == "float":
                        u = read_f32(gxx)
                        v = read_f32(gxx)
                        # vertex_string += f"UV:({u:.6f}, {v:.6f}) "

                    if color_type == "BGR 565":
                        # TODO
                        color = read_u16(gxx)
                        # print(f"{color:X}")
                        # print(f"{bgr_to_rgba(color):X}")
                        # exit()
                        vertex_string += f"bgr:0x{color:X} "
                    elif color_type == "ABGR 8888":
                        color = read_u32(gxx)
                        vertex_string += f"abgr:0x{color:X} "

                    x, y, z = 0.0, 0.0, 0.0
                    if position_type == "float":
                        x = read_f32(gxx)
                        y = read_f32(gxx)
                        z = read_f32(gxx)
                        # vertex_string += f"pos:({x:.6f}, {y:.6f}, {z:.6f})"

                    if position_type == "float":
                        vertex_string += f"{x:.6f} {y:.6f} {z:.6f}"
                    if texcoord_type == "float":
                        vertex_string += f" {u:.6f} {v:.6f}"
                    values += "\n" + vertex_string

                vertex_addr += block_size * count

            case GECommand.GE_JUMP.value:
                addr = (buffer << 8 & 0xFFFFFFFF) >> 8
                return_addr.append(gpu_offset)
                gpu_offset = addr
                # values = f"Jump to: 0x{addr:X}"
                values = ""

            case GECommand.GE_CALL.value:
                addr = (buffer << 8 & 0xFFFFFFFF) >> 8
                return_addr.append(gpu_offset)
                gpu_offset = addr
                # values = f"Call to: 0x{addr:X}"
                values = ""

            case GECommand.GE_RET.value:
                if len(return_addr) > 0:
                    addr = return_addr[-1]
                    del return_addr[-1]
                    gpu_offset = addr
                    # values = f"Return to: 0x{addr:X}"
                # else:
                #     values = "Nowhere to return"
                values = ""

            case GECommand.GE_BASE.value:
                addr = (buffer << 8 & 0xFFFFFFFF) >> 8
                # values = f"Set base addr to: 0x{addr:X}"
                values = ""

            case GECommand.GE_VERTEXTYPE.value:
                # Clear vertex type
                texcoord_type = "NULL"
                color_type = "NULL"
                position_type = "NULL"

                op = buffer
                vertex_type_string = "SetVertexType: VERTEX"

                through = (op & GE_VTYPE_THROUGH_MASK) == GE_VTYPE_THROUGH
                tc = (op & GE_VTYPE_TC_MASK) >> GE_VTYPE_TC_SHIFT
                col = (op & GE_VTYPE_COL_MASK) >> GE_VTYPE_COL_SHIFT
                nrm = (op & GE_VTYPE_NRM_MASK) >> GE_VTYPE_NRM_SHIFT
                pos = (op & GE_VTYPE_POS_MASK) >> GE_VTYPE_POS_SHIFT
                weight = (op & GE_VTYPE_WEIGHT_MASK) >> GE_VTYPE_WEIGHT_SHIFT
                weight_count = (
                    (op & GE_VTYPE_weight_count_MASK) >> GE_VTYPE_weight_count_SHIFT
                ) + 1
                morph_count = (
                    op & GE_VTYPE_morph_count_MASK
                ) >> GE_VTYPE_morph_count_SHIFT
                idx = (op & GE_VTYPE_IDX_MASK) >> GE_VTYPE_IDX_SHIFT

                color_names = [
                    "NULL",
                    "unsupported1",
                    "unsupported2",
                    "unsupported3",
                    "BGR 565",
                    "ABGR 1555",
                    "ABGR 4444",
                    "ABGR 8888",
                ]
                type_names = [
                    "NULL",
                    "u8",
                    "u16",
                    "float",
                ]
                type_namesI = [
                    "NULL",
                    "u8",
                    "u16",
                    "u32",
                ]
                type_namesS = [
                    "NULL",
                    "s8",
                    "s16",
                    "float",
                ]

                if through:
                    vertex_type_string += "through, "
                if type_names[tc] != "NULL":
                    # vertex_type_string += f"{type_names[tc]} texcoords, "
                    vertex_type_string += "|TEXCOORD"
                    texcoord_type = type_names[tc]

                if color_names[col] != "NULL":
                    vertex_type_string += f"{color_names[col]} colors, "
                    color_type = color_names[col]

                if type_names[nrm] != "NULL":
                    vertex_type_string += f"{type_namesS[nrm]} normals, "

                if type_names[pos] != "NULL":
                    # vertex_type_string += f"{type_namesS[pos]} positions, "
                    position_type = type_namesS[pos]

                if type_names[weight] != "NULL":
                    vertex_type_string += (
                        f"{type_names[weight]} weights {weight_count}, "
                    )
                elif weight_count > 1:
                    vertex_type_string += f"unknown weights {weight_count}, "

                if morph_count > 0:
                    vertex_type_string += f"{morph_count} morphs, "

                if type_namesI[idx] != "NULL":
                    vertex_type_string += f"{type_namesI[idx]} indexes"

                values = vertex_type_string

            case GECommand.GE_TEXTUREMAPENABLE.value:
                flag = (buffer << 8 & 0xFFFFFFFF) >> 8
                # values = f"Texture map enable: {flag:X}"
                values = ""

            case GECommand.GE_WORLDMATRIXNUMBER.value:
                f = buffer << 8 & 0xFFFFFFFF

                values = f"World: #{int(u32_to_f32(f))}, BONE DATA:\n"

                matrix = BoneMatrix()

                matrix.basisX_x = u32_to_f32(
                    read_u32(gxx, gpu_offset) << 8 & 0xFFFFFFFF
                )
                matrix.basisX_y = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x04) << 8 & 0xFFFFFFFF
                )
                matrix.basisX_z = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x08) << 8 & 0xFFFFFFFF
                )

                matrix.basisY_x = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x0C) << 8 & 0xFFFFFFFF
                )
                matrix.basisY_y = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x10) << 8 & 0xFFFFFFFF
                )
                matrix.basisY_z = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x14) << 8 & 0xFFFFFFFF
                )

                matrix.basisZ_x = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x18) << 8 & 0xFFFFFFFF
                )
                matrix.basisZ_y = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x1C) << 8 & 0xFFFFFFFF
                )
                matrix.basisZ_z = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x20) << 8 & 0xFFFFFFFF
                )

                matrix.translation_x = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x24) << 8 & 0xFFFFFFFF
                )
                matrix.translation_y = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x28) << 8 & 0xFFFFFFFF
                )
                matrix.translation_z = u32_to_f32(
                    read_u32(gxx, gpu_offset + 0x2C) << 8 & 0xFFFFFFFF
                )

                values += f"  Position: ({matrix.translation_x:.6f}, {matrix.translation_y:.6f}, {matrix.translation_z:.6f})\n"
                values += f"  Scale:    ({matrix.get_scale_x():.6f}, {matrix.get_scale_y():.6f}, {matrix.get_scale_z():.6f})\n"
                values += f"  Radians:  ({matrix.get_rotation().x:.6f}, {matrix.get_rotation().y:.6f}, {matrix.get_rotation().z:.6f})\n"
                values += f"  Degrees:  ({rad2deg(matrix.get_rotation().x):.6f}, {rad2deg(matrix.get_rotation().y):.6f}, {rad2deg(matrix.get_rotation().z):.6f})"

            case GECommand.GE_WORLDMATRIXDATA.value:
                data = buffer << 8 & 0xFFFFFFFF
                f = u32_to_f32(data)
                values = f"World matrix set: {f:.6f}"

            case GECommand.GE_TEXSCALEU.value:
                f = buffer << 8 & 0xFFFFFFFF
                # values = f"Texture U scale: {u32_to_f32(f):.6f}"
                values = ""

            case GECommand.GE_TEXSCALEV.value:
                f = buffer << 8 & 0xFFFFFFFF
                # values = f"Texture V scale: {u32_to_f32(f):.6f}"
                values = ""

            case GECommand.GE_TEXOFFSETU.value:
                f = buffer << 8 & 0xFFFFFFFF
                # values = f"Texture U offset: {u32_to_f32(f):.6f}"
                values = ""

            case GECommand.GE_TEXOFFSETV.value:
                f = buffer << 8 & 0xFFFFFFFF
                # values = f"Texture V offset: {u32_to_f32(f):.6f}"
                values = ""

            case GECommand.GE_MATERIALAMBIENT.value:
                color = (buffer << 8 & 0xFFFFFFFF) >> 8
                values = f"Material ambient color: 0x{color:X}"

            case GECommand.GE_MATERIALALPHA.value:
                color = (buffer << 8 & 0xFFFFFFFF) >> 8
                values = f"Material alpha color: 0x{color:X}"

            case _:
                # if new instruction will be found, GXXTool will output list of new instructions after parsing finished
                data = buffer >> 24
                unk_instr.add(data)

        if len(return_addr) > 0:
            # if GE perform ump or call, we should not count until it returns to animation data block
            j -= 1
        buffer = read_u32(gxx, gpu_offset)

        for instr in unk_instr:
            # output list of new found instructions
            print(f"Unknown istruction found: 0x{instr:X}")

        j += 1

        if values:
            offsets_values[gpu_offset] = values

offsets_values = dict(sorted(offsets_values.items()))
for gpu_offset, values in offsets_values.items():
    print(f"0x{gpu_offset:X} > {values}")
