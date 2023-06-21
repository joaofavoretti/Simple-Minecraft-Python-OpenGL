attribute vec3 position;
attribute vec3 normal;
attribute vec2 texture;
varying vec2 out_texture;
varying vec3 out_frag_pos;
varying vec3 out_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main(){
    gl_Position = projection * view * model * vec4(position,1.0);
    out_texture = vec2(texture);
    out_frag_pos = position;
    out_normal = normal;
}
