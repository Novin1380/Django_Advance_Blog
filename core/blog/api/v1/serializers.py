from rest_framework import serializers
from ...models import Post,Category
from accounts.models import Profile,User


class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField()   # or using charfield(read_only=True)
    relative_url = serializers.URLField(source = 'get_api_absolute_url',read_only = True)
    snippet = serializers.ReadOnlyField(source = 'get_snippet')
    absolute_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(many=False,slug_field='name',queryset = Category.objects)
    
    
    class Meta:
        model = Post
        fields = ["id","author",'image',"title","category","content",'relative_url','absolute_url',"snippet","created_date","status","published_date"]
        read_only_fields = ['author',]
        
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet',None)
            rep.pop('relative_url',None)
            rep.pop('absolute_url',None)
        else:
            rep.pop('content',None)
            
        rep['category'] = CategorySerializer(instance.category,context = {'request': request}).data
        
        return rep
    
    def create(self, validated_data):
        try:
            validated_data["author"] = Profile.objects.get(
                user__id=self.context.get("request").user.id
            )
        except:
            validated_data["author"] = Profile.objects.get(
                id=self.context.get("request").user.id
            )
        print(self.context.get("request").user.id)
        
        ######### Second way is define user separately #########
        # user = User.objects.get(id = self.context.get("request").user.id)

        # validated_data["author"] = Profile.objects.get(
        #     user__id=user
        # )
        return super().create(validated_data)

    

        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
       
# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)