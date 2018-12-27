#version 330 core

out vec4 FragColor;

in vec3 LightingColor; 
in vec2 TexCoord;

uniform vec3 objectColor;
uniform sampler2D ourTexture;

void main()
{
   FragColor = vec4(LightingColor * objectColor, 1.0) * texture(ourTexture, TexCoord);
}