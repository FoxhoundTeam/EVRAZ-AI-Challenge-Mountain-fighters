from src.base.models import Employee, Camera, Violation, Frame
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
import jwt

from src.settings import CENTRIFUGO_JWT_SECRET

class EmployeeSeializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['last_frame'] = StaticFrameSerializer(instance=Frame.objects.filter(camera_id=data['id']).order_by('dttm').last()).data

        return data

class CameraStaticSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    code = serializers.CharField()
    work_shop_name = serializers.CharField(source='work_shop.name')

class StaticFrameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    photo = serializers.ImageField(read_only=True)
    dttm = serializers.DateTimeField()

class FrameSerializer(serializers.ModelSerializer):
    camera_code = serializers.CharField(required=False, write_only=True)
    camera = CameraStaticSerializer()
    class Meta:
        model = Frame
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('camera_code') and not attrs.get('camera_id'):
            code = attrs.get('camera_code')
            camera = Camera.objects.filter(code=code).first()
            if not camera:
                raise serializers.ValidationError(f'Camera with code {code} doesn\'t exist')
            attrs['camera_id'] = camera.id
        return attrs
    
    
    def create(self, validated_data):
        instace = super().create(validated_data)
        instace.save(send_to_socket=True)
        return instace


class ViolationSerializer(serializers.ModelSerializer):
    employee = EmployeeSeializer()
    frame = FrameSerializer()
    class Meta:
        model = Violation
        fields = '__all__'

class ChartSerializer(serializers.Serializer):
    dt_from = serializers.DateField()
    dt_to = serializers.DateField()

class UserSerializer(UserDetailsSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['token'] = jwt.encode({"sub": str(instance.id)}, CENTRIFUGO_JWT_SECRET).decode()
        return ret
