
import matplotlib.pyplot as plt

from wordshifts import WordShifts

# Load demo data
sampleText = ''
with open('Nov.txt','r') as fl:
    for line in fl:
        sampleText += line.strip()
print len(sampleText)
wShift = WordShifts()
wsData = wShift.computeWordShifts(sampleText[:10000], sampleText[-5000:])

print wsData['arousal']

vals = list()
for w,d in wsData['arousal']['word_shift'].items():
    vals.append(d['shift'])
print sorted(vals)
print sum(vals)
def plot_wordshift(wordShift, params={}):
    
    topN = params.get('topN', 50)
    shifts = list()
    sortedWords = list()
    for w in sorted(wordShift['word_shift'].items(), 
                    key=lambda x: abs(x[1]['shift']), 
                    reverse=True):
        sortedWords.append(w[0])
        shifts.append(wordShift['word_shift'][w[0]]['shift'])
    dVals = shifts[:topN]
    sortedWords = sortedWords[:topN]
    
    fig = plt.figure(figsize=params.get('figsize',(4,8)))
    #axSummary = fig.add_axes(params.get('rect_summary',[0.,0.9,1.,0.1]))
    #axSummary.set_xticks([])
    #axSummary.set_yticks([])
    #axSummary.set_xlim([-100,100])
    
    #axShifts = fig.add_axes(params.get('rect_shifts',[0.,0.,1.,0.9]))
    axShifts = fig.add_axes(params.get('rect_shifts',[0.,0.,1.,1.]))
    barlist = axShifts.barh(range(1,topN+1), dVals,
                  align='center', linewidth=0, alpha=0.5, color='r')
    axShifts.set_ylim(axShifts.get_ylim()[::-1])
    for i,w in enumerate(sortedWords):
        case = wordShift['word_shift'][w]['case'].replace('u','\\uparrow').replace('d','\\downarrow')
        shift = wordShift['word_shift'][w]['shift']
        
        barlist[i].set_color('b' if case[0] == '+' else 'y')
        if shift > 0:
            axShifts.text(shift, i+1, r' {} ${}$'.format(w, case), 
                          color='0.0' if '+' in case else '0.5',
                          va='center', ha='left')
        else:
            axShifts.text(shift, i+1, r'${}$ {} '.format(case, w), 
                          color='0.0' if '+' in case else '0.5',
                          va='center', ha='right')
    
    #axShifts.set_xticks([])
    #axShifts.set_yticks([])
    #axShifts.set_xlim([-100,100])
    xmax = 1.5 * max([abs(x) for x in axShifts.get_xlim()])
    axShifts.set_xlabel('Per word avg. sentiment shift (%)', fontsize=14)
    axShifts.set_ylabel('Word rank', fontsize=14)
    axShifts.set_xlim([-xmax,xmax])
    axShifts.set_ylim([topN+1, 0])
    axShifts.tick_params(axis='both', which='major', labelsize=12)
    
    if params.get('rect_cumulative',True) <> False:
        axCumulative = fig.add_axes(params.get('rect_cumulative',[.1, 0.1, .17, .2]))
        csum = np.cumsum(shifts)
        axCumulative.plot(csum, range(len(csum)), c='k')
        axCumulative.axhline(topN)
        axCumulative.set_yscale('log')
        if sum(shifts) > 0:
            axCumulative.set_xticks([0,100])
            axCumulative.set_xticklabels([0,100])
            axCumulative.set_xlim((0,sum(shifts)))
        else:
            axCumulative.set_xticks([-100,0])
            axCumulative.set_xticklabels([-100,0])
            axCumulative.set_xlim((sum(shifts),0))
        axCumulative.invert_yaxis()
        axCumulative.set_xlabel(r'$\sum_{i=1}^r \delta h_{avg,i}$',fontsize=12)
        axCumulative.tick_params(axis='both', which='major', labelsize=8)
        
    #if params.get('rect_size', True) <> False:
    #    axSize = fig.add_axes(params.get('rect_size',[.7, .05, .25, .125]))
    #    axSize.set_xticks([])
    #    axSize.set_yticks([])
        
    if 'title' in params:
        axShifts.set_title(params['title'], fontsize=14)
        
    if 'savefig' in params:
        plt.savefig(params['savefig'], bbox_inches='tight', dpi=300)
        
    
#wShift = WordShifts()
#wsData = wShift.computeWordShifts(sampleText[-int(len(sampleText)*0.1):],
#                                  sampleText[:int(len(sampleText)*0.1)])
    
plot_wordshift(wsData['happiness'], params={'topN':50, 'rect_cumulative':False, 'savefig':'Nov'})
# plt.show()
