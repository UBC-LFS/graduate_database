from django.views import View
from django.shortcuts import render

from gp_admin import api


def index(request):
    print( request.session.get('loggedin_user') )
    
    return render(request, 'gp_supervisor/index.html')


class GetGradSupervision(View):
    def get(self, request, *args, **kwargs):
        
        prof = api.get_professor_by_username(request.user.username)
        print(request.user.username, prof)

        supervisions = []
        non_supervisors = 0
        num_supervisors = 1
    
        num_students = prof.supervision_set.count()
        if num_students > 0:
            prof_id = prof.id
            prof_full_name = prof.get_full_name()
            prof_title = prof.title.name
            prof_position = prof.position.name

            i = 0
            for sup in prof.supervision_set.all():
                if i > 0:
                    prof_id = None
                    prof_full_name = None
                    prof_title = None
                    prof_position = None
                    non_supervisors += 1
                i += 1

                supervisions.append({
                    'prof_id': prof_id,
                    'prof_full_name': prof_full_name,
                    'prof_title': prof_title,
                    'prof_position': prof_position,
                    'num_students': num_students,
                    'prof_role': sup.professor_role.name,
                    'stud_full_name': sup.student.get_full_name(),
                    'stud_current_degree': sup.student.current_degree,
                    'stud_program_code': sup.student.program_code,
                    'created_on': sup.created_on,
                    'updated_on': sup.updated_on,
                    'num_supervisors': num_supervisors,
                    'odd_or_even': 'odd' if num_supervisors % 2 != 0 else 'even'
                })
            num_supervisors += 1

        return render(request, 'gp_supervisor/get_grad_supervision.html', {
            'supervisions': supervisions,
            'total_supervisions': num_supervisors
        })

