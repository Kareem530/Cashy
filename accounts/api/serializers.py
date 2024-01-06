from accounts.models import User
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','phonenum','email', 'password', 'password2','balance']
        extra_kwargs = {
            'password' : {'write_only': True},
            'balance' : {'read_only': True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phonenum_pattern = r'^01[0-2][0-9]{8}$'

        if password != password2:
            raise serializers.ValidationError({'Error': 'Passwords do not match'})
        
        if not re.match(email_pattern, self.validated_data['email']):
         raise serializers.ValidationError({'Error': 'Please enter a valid email address'})
     
        if not re.match(phonenum_pattern, self.validated_data['phonenum']):
         raise serializers.ValidationError({'Error': 'Please enter a valid Egyptian phone number'})     

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error': 'Email already exists!'})
        
        if User.objects.filter(phonenum=self.validated_data['phonenum']).exists():
            raise serializers.ValidationError({'Error': 'Phone Number already exists!'})
        
        account = User(first_name = self.validated_data['first_name'] ,last_name = self.validated_data['last_name'] ,email=self.validated_data['email'], username=self.validated_data['username'],phonenum=self.validated_data['phonenum'])
        account.set_password(password)
        account.save()

        return account