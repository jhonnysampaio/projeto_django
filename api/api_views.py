from rest_framework import generics
from django.shortcuts import render
from gerenciamento_escola.models import Aluno, Curso, Matricula
from .serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
import json

class AlunoListarCriar(generics.ListCreateAPIView):
  queryset = Aluno.objects.all()
  serializer_class = AlunoSerializer

class AlunoRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  queryset = Aluno.objects.all()
  serializer_class = AlunoSerializer

class CursoListaCriar(generics.ListCreateAPIView):
  queryset = Curso.objects.all()
  serializer_class = CursoSerializer

class CursoRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  queryset = Curso.objects.all()
  serializer_class = CursoSerializer

class MatriculaCriar(generics.ListCreateAPIView):
  queryset = Matricula.objects.all()
  serializer_class = MatriculaSerializer

class MatriculaPorAluno(generics.ListAPIView):
  serializer_class = MatriculaSerializer

  def get_queryset(self):
    aluno_id =self.kwargs["aluno_id"]
    return Matricula.objects.filter(aluno_id=aluno_id)

class MatriculaRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  queryset = Matricula.objects.all()
  serializer_class = MatriculaSerializer
  lookup_field = "pk"

class Relatorio(APIView):
  def get(self, request):
    alunos = Aluno.objects.all()
    relatorio = []

    tot_alunos = Aluno.objects.count()
    tot_pendencias = 0.0

    for aluno in alunos:
      matriculas = Matricula.objects.filter(aluno=aluno)

      tot_devido = sum(float(m.curso.valor_inscricao) for m in matriculas)
      pendente = sum(float(m.curso.valor_inscricao) for m in matriculas if not m.status_pagamento != "pago")

      tot_pendencias += float(pendente)

      relatorio.append({
        "aluno" : aluno.nome,
        "email" : aluno.email,
        "total_devido"  : float(tot_devido),
        "pagamentos_pendentes" : float(pendente),
        "cursos" : [
          {
            "curso" : m.curso.nome,
            "valor" : float(m.curso.valor_inscricao),
            "status_pagamento" : m.status_pagamento
          }
          for m in matriculas
        ]


      })

    data = { 
      "total_alunos" : tot_alunos,
      "total_pendencias_geral" : float(tot_pendencias),
      "detalhes" : relatorio
    }

    return Response(data)


class RelatorioDownload(APIView):
  def get(self, request):
    response_data = Relatorio().get(request).data

    response = HttpResponse(
      json.dumps(response_data, indent=4, ensure_ascii=False),
      content_type = "application/json"
    )

    response["Content-Disposition"] = "attachment; filename=relatorio.json"

    return response
  
def RelatorioRaw(request):
  sql = """
SELECT
  m.id,
  a.nome AS aluno_nome,
  a.cpf,
  c.nome AS curso_nome,
  c.valor_inscricao,
  m.status_pagamento,
  m.data_matricula

FROM gerenciamento_escola_matricula m
INNER JOIN gerenciamento_escola_aluno a ON a.id = m.aluno_id
INNER JOIN gerenciamento_escola_curso c ON c.id = m.curso_id
ORDER BY m.data_matricula DESC  
"""
  relatorio = Matricula.objects.raw(sql)

  dados = [
    {
      "id" : item.id,
      "aluno" : item.aluno_nome,
      "cpf" : item.cpf,
      "curso" : item.curso_nome,
      "valor_inscricao" : float(item.valor_inscricao),
      "status_pagamento" : item.status_pagamento,
      "data_matricula" : str(item.data_matricula)
    }
    for item in relatorio
  ]

  if request.GET.get("format") == "json":
    return JsonResponse(dados, safe=False)
  
  return render(request, "api/relatorio_draw.html", {"dados" : dados})