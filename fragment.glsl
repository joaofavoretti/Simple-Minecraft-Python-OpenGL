uniform vec3 lightDir; // define coordenadas de posicao da luz
uniform float ka; // coeficiente de reflexao ambiente
uniform float kd; // coeficiente de reflexao difusa

vec3 lightColor = vec3(1.0, 1.0, 1.0);

varying vec2 out_texture; // recebido do vertex shader
varying vec3 out_normal; // recebido do vertex shader
varying vec3 out_fragPos; // recebido do vertex shader
uniform sampler2D samplerTexture;
 
 
 
void main(){
    vec3 ambient = ka * lightColor;             

    vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
    float diff = max(dot(norm, normalize(lightDir)), 0.0); // verifica limite angular (entre 0 e 90)
    vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
     
    vec4 texture = texture2D(samplerTexture, out_texture);
    vec4 result = vec4((ambient + diffuse),1.0) * texture; // aplica iluminacao
    gl_FragColor = result;
}
