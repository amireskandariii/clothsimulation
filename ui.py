'''
only need to install the following modules, code should run
pip install PyOpenGL
pip install glfw
pip install numpy
'''
import sys

from OpenGL import GL as gl
import glfw
from OpenGL.GLU import *
import numpy as np

#gen the cloth
import cloth as Cloth
cloth = Cloth.Cloth()
dragged_point = None
dragged_mass = None

# Rendering-related Code ------------------------------------------------------------
'''for capture screen shots'''
def dump_framebuffer_to_ppm(ppm_name, fb_width, fb_height):
    pixelChannel = 3
    pixels = gl.glReadPixels(0, 0, fb_width, fb_height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    fout = open(ppm_name, "w")
    fout.write('P3\n{} {}\n255\n'.format(int(fb_width), int(fb_height)))
    for i in range(0, fb_height):
        for j in range(0, fb_width):
            cur = pixelChannel * ((fb_height - i - 1) * fb_width + j)
            fout.write('{} {} {} '.format(int(pixels[cur]), int(pixels[cur+1]), int(pixels[cur+2])))
        fout.write('\n')
    fout.flush()
    fout.close()

screen_width, screen_height = 1024, 512
x_mid = x_size = screen_width/2
y_mid = y_size = screen_height/2
ss_id = 0 # screenshot id

''' create window'''
if not glfw.init():
    sys.exit(1)

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
title = 'Cloth Canvas'
window = glfw.create_window(screen_width, screen_height, title, None, None)
if not window:
    print('GLFW Window Failed')
    sys.exit(2)
glfw.make_context_current(window)
gl.glClearColor(0.3, 0.4, 0.5, 0)

shaders = {
    gl.GL_VERTEX_SHADER: '''\
    #version 330 core
    layout(location = 0) in vec3 aPos;
    void main() {
        gl_Position = vec4(aPos, 1);
    }
''',
    gl.GL_FRAGMENT_SHADER: '''\
    #version 330 core
    out vec3 color;
    void main() {
      color = vec3(0.9,0.8,0.7);
    }
'''}

program_id = gl.glCreateProgram()
shader_ids = []
for shader_type, shader_src in shaders.items():
    shader_id = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader_id, shader_src)
    gl.glCompileShader(shader_id)
    # check if compilation was successful
    result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
    nlog = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
    if nlog:
        logmsg = gl.glGetShaderInfoLog(shader_id)
        print("Shader Error", logmsg)
        sys.exit(1)
    gl.glAttachShader(program_id, shader_id)
    shader_ids.append(shader_id)

gl.glLinkProgram(program_id)
result = gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS)
nlog = gl.glGetProgramiv(program_id, gl.GL_INFO_LOG_LENGTH)
if nlog:
    logmsg = gl.glGetProgramInfoLog(program_id)
    print("Link Error", logmsg)
    sys.exit(1)
gl.glUseProgram(program_id)

def draw_data(data, DRAW_MODE=gl.GL_POINTS, point_size=1):
    if data == None:
        return
    pt_number = int(len(data)/3)
    if pt_number == 0:
        return

    vertex_array_id = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vertex_array_id)
    attr_id = 0
    vertex_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
    array_type = (gl.GLfloat * len(data))
    sizeof_float = ctypes.sizeof(ctypes.c_float)
    gl.glBufferData(gl.GL_ARRAY_BUFFER,
                    len(data) * sizeof_float,
                    array_type(*data),
                    gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(
        attr_id,  # attribute 0.
        3,  # components per vertex attribute
        gl.GL_FLOAT,  # type
        False,  # to be normalized?
        0,  # stride
        None  # array buffer offset
    )
    gl.glEnableVertexAttribArray(attr_id)
    gl.glPointSize(point_size)
    gl.glDrawArrays(DRAW_MODE, 0, pt_number)

def draw_cloth(cloth):
    lines = []

    for c in range(0, cloth.num_constraints):
        pt1 = cloth.springs[c].p1.pos
        pt2 = cloth.springs[c].p2.pos
        sx1, sy1 = cloth_to_screen(pt1[0], pt1[1])
        sx2, sy2 = cloth_to_screen(pt2[0], pt2[1])
        lines += [sx1, sy1, 0, sx2, sy2, 0]

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    if len(lines) > 0:
        draw_data(lines, gl.GL_LINES)

    if dragged_point:
        pos = dragged_point.pos
        x, y = cloth_to_screen(pos[0], pos[1])
        dragged_pos = [x, y, 0]
        draw_data(dragged_pos, gl.GL_POINTS, 10)

# end of Rendering-related Code ------------------------------------------------------------

def screen_to_cloth(screen_x, screen_y):
    cloth_x = (screen_x/1.5) + 0.5
    cloth_y = (screen_y/-1.5) + 0.5
    return cloth_x, cloth_y

def cloth_to_screen(cloth_x, cloth_y):
    screen_x = 1.5*(cloth_x -0.5)
    screen_y = -1.5*(cloth_y -0.5)
    return screen_x, screen_y

lbutton_down = False
def mouse_button_callback(window, button, action, mods):
    global key_points, lbutton_down, dragged_point, dragged_mass
    x_pos, y_pos = glfw.get_cursor_pos(window)
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        print('right button at', x_pos, y_pos)
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x_click = (x_pos-x_mid)/x_size
        y_click = -(y_pos-y_mid)/y_size
        cx, cy = screen_to_cloth(x_click, y_click)
        dragged_point = cloth.getClosestPoint(np.array([cx, cy]))
        dragged_mass = dragged_point.mass
        dragged_point.mass = float('inf')
        print('left button at', x_click, y_click)
        lbutton_down = True

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
        lbutton_down = False
        dragged_point.mass = dragged_mass
        print('release')

def cursor_pos_callback(window, x_pos, y_pos):
    x_hover = (x_pos - x_mid) / x_size
    y_hover = -(y_pos - y_mid) / y_size
    if lbutton_down and dragged_point:
        cx, cy = screen_to_cloth(x_hover, y_hover)
        dragged_point.pos = np.array([cx, cy])
    #print(x_hover, y_hover)




# run-time UI loop ---------------------------------------------------
glfw.set_mouse_button_callback(window, mouse_button_callback)
glfw.set_cursor_pos_callback(window, cursor_pos_callback)
while (
    glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
    not glfw.window_should_close(window)
):

    #press key p will capture screen shot
    if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
        print ("Capture Window ", ss_id)
        buffer_width, buffer_height = glfw.get_framebuffer_size(window)
        ppm_name = "CurveCanvas-ss" + str(ss_id) + ".ppm"
        dump_framebuffer_to_ppm(ppm_name, buffer_width, buffer_height)
        ss_id += 1

    cloth.update()
    draw_cloth(cloth)
    glfw.swap_buffers(window)
    glfw.poll_events()

#release resource
for shader_id in shader_ids:
    gl.glDetachShader(program_id, shader_id)
    gl.glDeleteShader(shader_id)
gl.glUseProgram(0)
gl.glDeleteProgram(program_id)