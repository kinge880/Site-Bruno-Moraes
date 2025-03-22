from collections import namedtuple
import operator
from django.db.models import Q
from functools import reduce
from django_serverside_datatable.datatable import DataTablesServer
from django.core.exceptions import FieldDoesNotExist
from django.db.models import ForeignKey
from django.forms.models import model_to_dict
from project import acessManager
from django.contrib.auth.decorators import login_required, permission_required

class dataTableServerPersonal(DataTablesServer):
    def __init__(self, request, columns, qs, columns_query, regiao):
        self.columns = columns
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.GET
        #self.regioes = acessManager.obterRegiao(request)
        if regiao != 'N':
            self.regioes = [regiao]
        # results from the db
        self.result_data = None
        # total in the table after filtering
        self.cardinality_filtered = 0
        # total in the table unfiltered
        self.cardinality = 0
        self.user = request.user
        self.qs = qs
        self.columns_query = columns_query
        self.run_queries()

    def run_queries(self):
        # pages has 'start' and 'length' attributes
        pages = self.paging()
        # the term you entered into the datatable search
        _filter, op = self.filtering()
        # the document field you chose to sort
        sorting = self.sorting()
        # custom filter
        qs = self.qs

        if _filter:
            if op == "or":
                data = qs.filter(
                    reduce(operator.or_, _filter)).order_by('%s' % sorting)
            else:
                data = qs.filter(
                    reduce(operator.and_, _filter)).order_by('%s' % sorting)
            len_data = data.count()
            if pages.length != -1:
                data = data[pages.start:pages.length].values(*self.columns)
            else:
                data = data.values(*self.columns)
        else:
            data = qs.order_by('%s' % sorting).values(*self.columns)
            len_data = data.count()
            _index = int(pages.start)
            if pages.length != -1:
                data = data[_index:_index + (pages.length - pages.start)]
        
        result = []
        modelo = qs.model
        campos = modelo._meta.fields
        chaves_estrangeiras = [campo for campo in campos if isinstance(campo, ForeignKey)]
        chave_primaria = ''
        for campo in campos:
            if campo.primary_key:
                chave_primaria = campo.name
        
        for query in data:
            for column_name, nome_coluna_destino in self.columns_query:
                if nome_coluna_destino:
                    for chave in chaves_estrangeiras:
                        if column_name == chave.name:
                            valorrelacionado = modelo.objects.filter(**{chave_primaria: query[chave_primaria]})
                            attr = getattr(valorrelacionado[0], column_name, None)
                            if attr is not None:
                                print(column_name)
                                print(nome_coluna_destino)
                                dictAttr = model_to_dict(attr)
                                query[column_name] = str(dictAttr[column_name]) + ' - ' + str(dictAttr[nome_coluna_destino])
            result.append(query)
        
        self.result_data = list(result)

        # length of filtered set
        if _filter:
            self.cardinality_filtered = len_data
        else:
            self.cardinality_filtered = len_data
        self.cardinality = pages.length - pages.start

    def output_result(self):
        output = dict()
        output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.qs.count())
        output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        data_rows = []

        for row in self.result_data:
            data_row = []
            for i in range(len(self.columns)):
                # val = getattr(row, self.columns[i])
                val = row[self.columns[i]]
                data_row.append(val)
            data_rows.append(data_row)
        output['aaData'] = data_rows
        return output

    
    def filtering(self):
        # build your filter spec
        or_filter = []
        op = ""
        if (self.request_values.get('sSearch')) and (self.request_values['sSearch'] != ""):
            op = "or"
            for i in range(len(self.columns_query)):
                if self.request_values['bSearchable_%d' % i] == 'true':
                    column_name = self.columns_query[i]
                    # Verificar se a coluna é uma chave estrangeira
                    try:
                        # Tenta acessar o campo diretamente na queryset
                        field = self.qs.model._meta.get_field(column_name[0]).get_internal_type()
                    except FieldDoesNotExist:
                        # Se a coluna não existir no modelo, pula para a próxima
                        continue
                    if str(field) == 'ForeignKey':
                        # Se for uma chave estrangeira, não uso icontains
                        or_filter.append(
                            Q(**{column_name[0] + '__'+column_name[1]+'__icontains': self.request_values['sSearch']}))
                    else:
                        or_filter.append(
                            Q(**{'%s__icontains' % column_name[0]: self.request_values['sSearch']}))
        else:
            op = "and"
            for i in range(len(self.columns_query)):
                if (self.request_values.get(f'sSearch_{i}')) and (self.request_values[f'sSearch_{i}'] != ""):
                    column_name = self.columns_query[i]
                    # Verificar se a coluna é uma chave estrangeira
                    try:
                        # Tenta acessar o campo diretamente na queryset
                        field = self.qs.model._meta.get_field(column_name[0])
                    except FieldDoesNotExist:
                        # Se a coluna não existir no modelo, pula para a próxima
                        continue
                    if str(field) == 'ForeignKey':
                        or_filter.append(
                            Q(**{column_name[0] + '__'+column_name[1]+'__icontains': self.request_values['sSearch']}))
                    else:
                        or_filter.append(
                            (column_name[0] + '__icontains', self.request_values[f'sSearch_{i}']))
        
        q_list = [Q(x) for x in or_filter]
        return q_list, op