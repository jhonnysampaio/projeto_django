from django import forms
from .models import Aluno, Curso, Matricula

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "email", "cpf"]

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "carga_horaria", "valor_inscricao", "status"]

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ["aluno", "curso", "data_matricula", "status_pagamento"]
        