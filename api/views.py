from api.serializers import ExternalProgramSerializer
from core.utils import get_first_object_or_none, get_ip_address
from program.models import ExternalProgram, ExternalLogs
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


def check_banned(banned_list_key, check_parameter):
    banned_obj = get_first_object_or_none(ExternalProgram.objects, name=banned_list_key)
    banned_list = banned_obj.parameter if banned_obj else ''
    banned_list = banned_list.split(',')
    banned_list = [x.strip() for x in banned_list]

    return True if check_parameter in banned_list else False


def create_log(key, parameter, program, ip_address, success, save_log):
    if save_log:
        ExternalLogs.objects.create(
            name=key,
            parameter=parameter,
            program=program,
            ip_address=ip_address,
            success=success,
        )


class ExternalProgramView(views.APIView):
    model = ExternalProgram
    serializer_class = ExternalProgramSerializer
    permission_classes = []

    def get(self, format=None):
        ip_address = get_ip_address(self.request)

        save_log = get_first_object_or_none(ExternalProgram.objects, name='save_log')
        save_log = save_log.parameter.lower() if save_log else ''
        save_log = True if save_log == 'true' else False

        log_error = get_first_object_or_none(ExternalProgram.objects, name='log_error')
        log_error = log_error.parameter.lower() if log_error else ''
        log_error = True if log_error == 'true' else False

        obj_count = ExternalLogs.objects.count()
        limit = 500
        if obj_count > limit:
            rows = ExternalLogs.objects.all()[:limit].values_list('id', flat=True)  # only retrieve ids.
            ExternalLogs.objects.exclude(pk__in=list(rows)).delete()

        key = None
        program = None
        try:
            key = self.request.data.get('key', '')
            program = self.request.data.get('program', '')

            if not key or not program:
                create_log(key, 'missing_parameters', program, ip_address, False, save_log)
                return Response(
                    {
                        'success': False,
                        'message': 'Missing Parameters',
                        'data': [],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if key == 'all':
                create_log(key, '__All_Parameters_Sent__', program, ip_address, True, save_log)
                settings = self.model.objects.all()
                serializer = self.serializer_class(settings, read_only=True, many=True)
                return Response(serializer.data)
            else:
                setting = get_first_object_or_none(self.model.objects, name=key)

                if not setting:
                    create_log(key, 'invalid_key', program, ip_address, False, save_log)
                    return Response(
                        {
                            'success': False,
                            'message': 'Invalid Key',
                            'data': [],
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                banned_program = check_banned('banned_programs', program)
                create_log(key, 'Banned_Program', program, ip_address, False, banned_program and save_log)
                banned_ip = check_banned('banned_ips', ip_address)
                create_log(key, 'Banned_IP', program, ip_address, False, banned_ip and save_log)
                if banned_program or banned_ip:
                    return Response(
                        {
                            'success': False,
                            'message': 'Banned',
                            'data': [],
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                create_log(key, setting.parameter, program, ip_address, True, save_log)
                serializer = self.serializer_class([setting], many=True)
                return Response(
                    {
                        'success': True,
                        'data': serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            try:
                create_log(key if key else '', str(e), str(program), ip_address, False, log_error)
            except:
                create_log(key if key else '', str(e), str(program), '', False, log_error)

            return Response(
                {
                    'success': False,
                    'message': 'An error occurred. Please try again later.',
                    'data': [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
