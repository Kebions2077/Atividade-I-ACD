from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
g=p/'graficos'
d=pd.read_csv(p/'dados_benchmark.csv')
for a,x in d.groupby('algoritmo',sort=False):
 x.to_excel(p/f'{a}.ods',index=False,engine='odf')
 m=x.groupby(['N','ordem'],as_index=False).tempo_ms.mean()
 for ord in ['Crescente','Decrescente','Aleatoria','Repetidos']:
  z=m[m.ordem==ord].sort_values('N')
  if not z.empty: plt.plot(z.N,z.tempo_ms,marker='o',label=ord)
 plt.title(f'Tempo de execucao - {a}')
 plt.xlabel('Tamanho da entrada (N)')
 plt.ylabel('Tempo medio (ms)')
 plt.xscale('log')
 plt.xticks(sorted(x.N.unique()),[f'{int(n):,}'.replace(',','.') for n in sorted(x.N.unique())])
 plt.grid(True,alpha=.3); plt.legend(); plt.tight_layout()
 plt.savefig(g/f'{a}.png',dpi=150); plt.close()
r=d.groupby(['algoritmo','N','ordem'],as_index=False).agg(media_ms=('tempo_ms','mean'),maximo_ms=('tempo_ms','max'),minimo_ms=('tempo_ms','min'),desvio_padrao_ms=('tempo_ms','std'))
r.to_excel(p/'Resumo_Geral.ods',index=False,engine='odf')
print('Relatorios gerados.')