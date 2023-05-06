from rest_framework import serializers
from program.models import ExternalProgram


class ExternalProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalProgram
        fields = ('name', 'parameter',)
