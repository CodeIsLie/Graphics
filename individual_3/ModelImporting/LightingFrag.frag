#version 330 core

#define MAX_POINT_LIGHTS 4  

struct Material {

    sampler2D textureDiffuse1;
    sampler2D textureSpecular1;
    float shininess;
}; 

struct Light {
	vec3 ambient;
    vec3 diffuse;
    vec3 specular;
	
    vec3  position;
    vec3  direction;
    float cutOff;
	
	float constant;
    float linear;
    float quadratic;
};

struct DirLight {
    vec3 direction;
  
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};  

struct PointLight {    
    vec3 position;
    
    float constant;
    float linear;
    float quadratic;  

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
}; 

in vec2 TexCoords;
in vec3 Normal;
in vec3 FragPos;

out vec4 color;

uniform Light spotLight;
uniform PointLight pointLights[MAX_POINT_LIGHTS];
uniform DirLight dirLight;
uniform Material material;
uniform vec3 viewPos;

uniform int isOn;
uniform int useFlashlight;

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir);
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);
vec3 CalcSpotLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main() {
	vec3 norm = normalize(Normal);
	vec3 viewDir = normalize(viewPos - FragPos);
	if (isOn == 1) {
		// direct light
		vec3 result = CalcDirLight(dirLight, norm, viewDir);
		
		// point light
		for(int i = 0; i < MAX_POINT_LIGHTS; i++) {
			vec3 pointLight = CalcPointLight(pointLights[i], norm, FragPos, viewDir);
			if (pointLight.x > 0 || pointLight.y > 0 || pointLight.z > 0) {
				result += pointLight; 
			}
		}
		if (useFlashlight == 1) {
			// spot light
			result += CalcSpotLight(spotLight, norm, FragPos, viewDir);  
		}
		color = vec4(result, 1.0);		
    } else {
		vec3 l = CalcSpotLight(spotLight, norm, FragPos, viewDir);
		color = vec4(l, 1.0);
	}
}

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir) {
	vec3 lightDir = normalize(-light.direction);
	
    // diffuse
    float diff = max(dot(normal, lightDir), 0.0);
	
    // specular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
	
    // sum
    vec3 ambient  = light.ambient * vec3(texture(material.textureDiffuse1, TexCoords));
    vec3 diffuse  = light.diffuse  * diff * vec3(texture(material.textureDiffuse1, TexCoords));
    vec3 specular = light.specular * spec * vec3(texture(material.textureSpecular1, TexCoords));
    return (ambient + diffuse + specular);
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
	
    // diffuse
    float diff = max(dot(normal, lightDir), 0.0);
	
    // specular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
	
    // attenuation
    float distance    = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + 
  			     light.quadratic * (distance * distance));    
				 
    // sum
    vec3 ambient  = light.ambient  * vec3(texture(material.textureDiffuse1, TexCoords));
    vec3 diffuse  = light.diffuse  * diff * vec3(texture(material.textureDiffuse1, TexCoords));
    vec3 specular = light.specular * spec * vec3(texture(material.textureSpecular1, TexCoords));
    ambient  *= attenuation;
    diffuse  *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
}

vec3 CalcSpotLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir) {
	vec3 lightDir = normalize(light.position - fragPos);
	float theta = dot(lightDir, normalize(-light.direction));
	if(theta > light.cutOff) 
	{       
		float distance = length(light.position - fragPos);
		
		// diffuse
		float diff = max(dot(normal, lightDir), 0.0);
	
		// specular
		vec3 reflectDir = reflect(-lightDir, normal);
		float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
		float attenuation = 1.0 / (light.constant + light.linear * distance + 
					 light.quadratic * (distance * distance));    
					 
		// sum
		//vec3 ambient  = light.ambient  * vec3(texture(material.textureDiffuse1, TexCoords));
		vec3 diffuse  = light.diffuse  * diff * vec3(texture(material.textureDiffuse1, TexCoords));
		vec3 specular = light.specular * spec * vec3(texture(material.textureSpecular1, TexCoords));
		
		//ambient  *= attenuation;
		diffuse  *= attenuation;
		specular *= attenuation;
		
		return (diffuse + specular);
	}
	return light.ambient * vec3(texture(material.textureDiffuse1, TexCoords));
}
