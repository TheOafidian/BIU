from ..structures import Dataset2
from .. import formats
from .. import utils
from .. import ops
from .. import R

pd = utils.py.loadExternalModule("pandas")
sns = utils.py.loadExternalModule("seaborn")
plt = utils.py.loadExternalModule('matplotlib.pylab')

###############################################################################

def _load_all_q(excel):
    X = formats.XLSX(excel, data_only=True)
    Q = X['Sheet1']
    Q.columns = Q.iloc[0]
    Q = Q.iloc[1:]
    Q = Q.set_index(Q.columns[0])

    def try_cast_float(val):
        try:
            return float(val)
        except (ValueError, TypeError) as e:
            return None
        #etry
    #edef

    def try_cast_int(val):
        try:
            return int(val)
        except (ValueError, TypeError) as e:
            return None
        #etry
    #edef

    def try_cast_bool(val):
        if (val is None) or (str(val) == None):
            return None
        else:
            if isinstance(val, bool):
                return val
            elif isinstance(val, str):
                return val.lower() == 'true'
            else:
                return False
            #fi
        #fi
    #edef

    float_cols = [
        'Q1.BMI',
        'Q2.BMI',
         'Q1.Q28_1.Freq_Dairy_Probio',
         'Q1.Q28_2.Freq_Yoghurt_Probio',
         'Q1.Q28_3.Freq_Capsules_Probio',
         'Q1.Q29_1.Freq_Dairy',
         'Q1.Q29_2.Freq_FermFood',
         'Q1.Q29_3.Freq_EtOH',
         'Q1.Q29_4.Freq_Meat',
         'Q1.Q29_5.Freq_Animal_Prod',
         'Q1.Q29_6.Freq_Fish',
         'Q1.Q29_7.Freq_Sugar_Beverages',
         'Q1.Q29_8.Freq_Light_Beverages',
         'Q1.Q29_9.Freq_Fruit',
         'Q1.Q29_10.Freq_Vegetables',
         'Q2.Q10_1.Portion_24h_Dairy',
         'Q2.Q10_2.Portion_24h_Fermented_Food',
         'Q2.Q10_3.Portion_24h_Alcohol',
         'Q2.Q10_4.Portion_24h_Meat',
         'Q2.Q10_5.Portion_24h_Fish',
         'Q2.Q10_6.Portion_24h_Coffee',
         'Q2.Q10_7.Portion_24h_Sugar_Beverages',
         'Q2.Q10_8.Portion_24h_Light_Beverages',
         'Q2.Q10_9.Portion_24h_Fruit_Fibers',
         'Q2.Q10_10.Portion_24h_Vegetable_Fibers',
         'Q2.Q11_1.Portion_24h_Cold_Pasta',
         'Q2.Q11_2.Portion_24h_Whole_Grain_Bread',
         'Q2.Q11_3.Portion_24h_Sourdough',
         'Q2.Q11_4.Portion_24h_Quinoa',
         'Q2.Q11_5.Portion_24h_Seeds',
         'Q2.Q11_6.Portion_24h_Nuts',
         'Q2.Q11_7.Portion_24h_Chocolat',
         'Q2.Q11_8.Portion_24h_Candy',
         'Q2.Q11_9.Portion_24h_Salty_Snacks',
    ]
    int_cols = [
        'Q0.Leeftijd',
        'A.day_of_cycle',
        'Q1.Q50.Number_of_pregnancies',
        'Q1.Q6.Number_Of_Biological_Children'
    ]     

    bool_cols = [
        'Q2.Q25.Pill_progestogen',
        'Q2.Q25.Pill_combined',   
        'Q2.Q25.Pill_unknown',
        'Q2.Q25.Spiral_copper',
        'Q2.Q25.Spiral_hormone',
        'Q2.Q25.Prikpil',
        'Q2.Q25.Ring',
        'Q2.Q25.Implant',
        'Q2.Q25.Plaster',
        'Q2.Q25.Condom',
        'Q2.Q25.Cup',
        'Q2.Q25.Morning_after',
        'Q2.Q25.Periodic_celibacy',
        'Q2.Q25.Pullout',
        'Q2.Q25.Sterilized',    
        'Q2.Q25.Partner_sterilized',
        'Q1.Q32.Born_vaginal',
        'Q1.Q32.Born_csect',
        'Q1.Q32.Born_unknown',
        'A.Intercourse_yes',
        'A.Intercourse_no',
        'A.Intercourse_unknown',
        'Q1.Q50.Was_pregnant',
        'Q1.Q6.Has_children',
         'Q2.Q8_1.Intake_Probio_Dairy_24h',
         'Q2.Q8_4.Intake_Probio_Yoghurt_24h',
         'Q2.Q8_5.Intake_Probio_Capsules_24h',
         'Q2.Q8_6.No_Intake_Probio',
         'Q2.Q13.Intake_probiotics',
         'Q2.Delta_BMI',
    ]

    for col in Q.columns:
        if col in float_cols:
            Q[col] = Q[col].apply(try_cast_float).astype(float)
        elif col in int_cols:
            Q[col] = Q[col].apply(try_cast_int)
        elif col in bool_cols:
            Q[col] = Q[col].apply(try_cast_bool).astype('category')
        #fi
    #efor

    Q['Q2.Delta_BMI']        = Q.apply(lambda x: x['Q2.BMI'] - x['Q1.BMI'], axis=1)
    Q['Q1.Q50.Was_pregnant'] = Q['Q1.Q50.Number_of_pregnancies'].apply(lambda x: True if x > 0 else False)
    Q['Q1.Q6.Has_children']  = Q['Q1.Q6.Number_Of_Biological_Children'].apply(lambda x: True if x > 0 else False)
    Q['A.Critical_period']   = Q['A.day_of_cycle'].apply(lambda x: True if ((x >=14) & (x <= 18)) else False)

    return Q
#edef

###############################################################################

class ISALA(Dataset2):
    """
    An interface to the ISALA dataset.
    
    Typical usage:
    --------------
    goto = biu.db.GOTO2()
    
    # RNA-Seq expression data
    goto.expr   # Expression counts
    goto.blood  # Covariates for blood samples
    goto.muscle # Covariates for muscle samples
    
    # Genetic variation
    goto.filter(15, 50001000, 50005000)
    goto.filter_regions([(15, 50001000, 50005000),(13, 50001000, 50005000)])
    
    # Metabolomics data
    goto.metabolomics # Metabolyte measurements
    goto.metabolomics_cov # Covariates for metabolyte data
    """

    data_locations = {
        'Q'     : (_load_all_q,      utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/cleaned_surveys/flow1_all_questionnaires', 'xlsx')),
        'HQRA'  : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/hq_relative_abundances', 'pkl')),
        'HQRAG' : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/hq_relative_abundances_genus', 'pkl')),
        
        'HQS'   : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/hq_samples', 'pkl')),
        
        'PRA'   : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.pca.hqra',  'pkl')),
        'PRAG'  : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.pca.hqrag',  'pkl')),
        
        'TRA'   : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.tsne.hqra',  'pkl')),
        'TRAG'  : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.tsne.hqrag',  'pkl')),
        
        'URA'   : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.umap.hqra',  'pkl')),
        'URAG'  : (pd.read_pickle,   utils.fs.most_recent_file('/home/thies/repos/UA_isala/processed/embedding.umap.hqrag',  'pkl')),
        
        'rds_D'  : (None, '/home/thies/repos/UA_isala/data/16S/isala_cross_amplicon_20210225.rds'),
        'rds_DG' : (None, '/home/thies/repos/UA_isala/data/16S/isala_cross_amplicon_20210225_genus.rds'),
    }
    
    def __init__(self, *pargs, **kwargs):

        super(ISALA, self).__init__("ISALA/", *pargs, **kwargs)
        
        for d in self.data_locations:
            load_func, uri = self.data_locations[d]
            self._obj.add_file(d, utils.Acquire2(uri), finalize=False)
            if load_func is not None:
                self._obj.register(d, [d], lambda x, f=load_func, d=d: f(x[d]))
            #fi
        #efor
        biur = R.R()
        for objname, file, value in [ ('rds_S',  'rds_D', 'samples'),
                             ('rds_A',  'rds_D', 'abundances'),
                             ('rds_T',  'rds_D', 'taxa'),
                             ('rds_AG', 'rds_DG', 'abundances'),
                             ('rds_TG', 'rds_DG', 'taxa') ]:
            self._obj.register(objname, [file], 
                               lambda x, f=file, v=value : biur("""
                                   D <- readRDS('{file:s}')
                                   isala_r_get <- D${value:s}
            """.format(file=x[f], value=v)))
    #edef
    
    def plot_embedding(self, hue=None, palette='viridis', data='TSNE',
                       sample_meta=None, meta=None, meta_match='participant',
                       legend=False, title=None, d1='D1', d2='D2', *pargs, **kwargs):
        """
        plot_embedding
        
        parameters:
        -----------
        hue : string|list|None
            Describes colors for each point
            if string, then column in sample_meta or meta
            if list, then list of strings or numbers, of length equal to data
            if None, then no color is plotted
        palette : string
            color palette to use for hue, valid for plt.get_cmap
        data: pd.DataFrame|'TSNE'|'UMAP'|'PCA'
            dataset with embedding points to plot
            if pd.Dataframe, then use this data.
            if 'TSNE', use tsne embedding
            if 'UMAP', use umap embedding
            otherwise, use PCA embedding
        sample_meta : pd.DataFrame
            A dataframe with contains information PER SAMPLE IN DATA
        meta: pd.DataFrame
            A dataframe which contains information per sample, but is indexed on a different column
        meta_match : String
            The column by which meta is indexed, but exists in sample_meta
        legend: bool
            Plot a legend or not
        title: String
            Title for the plot
        d1,d2: Strings
            The names of the first and second components of the embedding to use
        *pargs, **kwargs : dicts
            additional arguments for seaborn.scatterplot
        
        """
        
        if sample_meta is None:
            sample_meta = self.HQS
        #fi
        
        if meta is None:
            meta = self.Q
        #fi
        
        if isinstance(data, str):
            data = data.lower()
            data = self.TRAG if data == 'tsne' else self.URAG if data == 'umap' else self.PRAG
        #fi
        
        re = data.copy()
        if hue is not None:
            try:
                if hue in sample_meta.columns:
                    re[hue] = sample_meta[hue]
                elif hue in meta.columns:
                    re[hue] = meta.loc[sample_meta[meta_match]][hue].values
            except TypeError:
                    re['hue'] = hue
                    hue = 'hue'
                #etry
            #fi
        #fi
        ax = sns.scatterplot(x=d1, y=d2, palette=palette, hue=hue, data=re, s=2, *pargs, **kwargs)

        if legend:
            if pd.api.types.is_numeric_dtype(re[hue]):
                norm = plt.Normalize(re[hue].min(), re[hue].max())
                sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
                if ax.get_legend() is not None:
                    ax.get_legend().remove()
                #fi
                ax.figure.colorbar(sm)
            else:
                ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol= 2)
            #fi
        elif hue is not None:
            ax.get_legend().remove()
        #fi

        if title:
            ax.set_title(title)
        #fi
    #edef
    
#eclass

###############################################################################