from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Curso, Matricula
from .forms import AlunoForm, CursoForm, MatriculaForm
# Create your views here.

def home(request):
    return render(request, "gerenciamento_escola/home.html")

def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    matriculas = Matricula.objects.filter(aluno=aluno).select_related("curso")

    tot_devido = sum(m.curso.valor_inscricao for m in matriculas)
    tot_pago = sum(
        m.curso.valor_inscricao for m in matriculas if m.status_pagamento == "pago"
    )

    context = {
        "aluno" : aluno,
        "matricula" : matriculas,
        "tot_devido" : tot_devido,
        "tot_pago" : tot_pago
    }

    return render (request, "alunos/historico_aluno.html", context)

def dashboard(request):
    tot_alunos = Aluno.objects.count()
    tot_matriculas =  Matricula.objects.count()

    matriculas_pagas = Matricula.objects.filter(status_pagamento="pago").count()
    matriculas_pendentes = Matricula.objects.filter(status_pagamento="pendente").count

    return render(request, "gerenciamento_escola/dashboard.html",{
        "tot_alunos" : tot_alunos,
        "tot_matriculas" : tot_matriculas,
        "matriculas_pagas" : matriculas_pagas,
        "matriculas_pendentes"  : matriculas_pendentes,
    })

def listar_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, "alunos/listar_alunos.html", {"alunos" : alunos})

def cadastrar_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:listar_alunos")
    
    else:
        form = AlunoForm()
    return render(request, "alunos/cadastrar_aluno.html", {"form" : form})

def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:listar_alunos")
        
    else:
        form = AlunoForm(instance=aluno)

    return render(request, "alunos/editar_aluno.html", {"form" : form, "aluno" : aluno})

def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.delete()

    return redirect("gerenciamento_escola:listar_alunos")

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, "cursos/listar_cursos.html", {"cursos" : cursos})

def cadastrar_curso(request):
    if request.method == "POST":
        form = CursoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:lista_cursos")
    
    else:
        form = CursoForm()
    return render(request, "cursos/cadastrar_curso.html", {"form" : form})

def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:listar_cursos")
    
    else:
        form = CursoForm(instance=curso)
    
    return render(request, "cursos/editar_curso.html", {"form" : form, "curso" : curso})

def excluir_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.delete()

    return redirect("gerenciamento_escola:listar_cursos")

def listar_matriculas(request):
    matriculas = Matricula.objects.all()
    return render(request, "matriculas/listar_matriculas.html", {"matriculas" : matriculas})

def cadastrar_matricula(request):
    if request.method == "POST":
        form = MatriculaForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:listar_matriculas")
        
    else:
        form = MatriculaForm()
    return render(request, "matriculas/cadastrar_matricula.html", {"form" : form})

def editar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)

    if request.method == "POST":
        form = MatriculaForm(request.POST, instance=matricula)

        if form.is_valid():
            form.save()

            return redirect("gerenciamento_escola:listar_matriculas")
    
    else:
        form = MatriculaForm()
    
    return render(request, "matriculas/editar_matricula.html", {"form" : form, "matricula" : matricula})

def excluir_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    matricula.delete()

    return redirect("gerenciamento_escola:listar_matriculas")