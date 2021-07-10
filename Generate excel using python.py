import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
bulk = pd.read_excel('dataoci/bulkQuery_result_7500w000001mavrAAA_7510w000001s2yUAAQ_7520w0000012aVh_so.xlsx')
bulk.rename(columns = {'OCE__Account__r.OCE__UniqueIntegrationID__c' : 'Account','OCE__Territories__c' : 'Territories'}, inplace = True)
ferring = pd.read_excel('dataoci/Ferring Business Administration Template_CUSTOMER ALIGNMENT RULES 20210302_so.xlsx')
ferring['Territories'] = ferring['Territories'].str.upper()
k=bulk.assign(Territories=bulk.Territories.str.split(";")).explode('Territories')
k['Territories'].replace('', np.nan, inplace=True)
k.dropna(subset=['Territories'], inplace=True)
k['Territories'] = k['Territories'].str.upper()
#####match -	matched accounts and matched territories) from both files.
out=pd.merge(k, ferring, on=['Account','Territories',], how='inner')
out.drop(['Id', 'OCE__ApprovalStatus__c','OCE__AddedTerritories__c','OCE__DroppedTerritories__c'], axis = 1,inplace=True) 
out=out.reindex(['Account','Territories','Operation'], axis=1)
out.to_excel('dataoci/output_matching_account_and_Territories.xlsx',index=False)
######-	matched accounts and unmatched territories from both files.

out_account=pd.merge(bulk, ferring, on='Account', how='inner')
out_account.drop(['Id', 'OCE__ApprovalStatus__c','OCE__AddedTerritories__c','OCE__DroppedTerritories__c','Territories_x'], axis = 1,inplace=True)
out_account.rename(columns = {'Territories_y' : 'Territories'}, inplace = True)
out_account= out_account.drop_duplicates()
out_unmat_terr_match_acc=pd.concat([k, out_account]).drop_duplicates(subset=["Territories"],keep=False)
out_unmat_terr_match_acc.drop(['Id', 'OCE__ApprovalStatus__c','OCE__AddedTerritories__c','OCE__DroppedTerritories__c'], axis = 1,inplace=True)
out_unmat_terr_match_acc=out_unmat_terr_match_acc.reindex(['Account','Territories','Operation'], axis=1)
out_unmat_terr_match_acc.to_excel('dataoci/output_matched accounts_and_unmatched_territories.xlsx',index=False)

####-	unmatched accounts from both files.
out_unmat=pd.concat([k, ferring]).drop_duplicates(subset=["Account"],keep=False)
out_unmat.drop(['Id', 'OCE__ApprovalStatus__c','OCE__AddedTerritories__c','OCE__DroppedTerritories__c'], axis = 1,inplace=True)
out_unmat=out_unmat.reindex(['Account','Territories','Operation'], axis=1)
out_unmat.to_excel('dataoci/output_account_unmatch.xlsx',index=False)

#####for duplicate accounts present in ‘bulk’  
out_dup_bulk = k[k.duplicated('Account',keep=False)]
out_dup_bulk.drop(['Id', 'OCE__ApprovalStatus__c','OCE__AddedTerritories__c','OCE__DroppedTerritories__c'], axis = 1,inplace=True)
out_dup_bulk=out_dup_bulk.reindex(['Account','Territories'], axis=1)
out_dup_bulk.to_excel('dataoci/output_dup_bulk.xlsx',index=False)

#####-Matched/unmatched accounts and unmatched territories  

out_mat_unmat_acc=pd.merge(out_unmat, ferring, on='Account', how='inner')
out_mat_unmat_acc.drop(['Territories_x','Operation_x'], axis = 1,inplace=True)
out_mat_unmat_acc= out_mat_unmat_acc.drop_duplicates()
out_mat_unmat_acc.rename(columns = {'Territories_y' : 'Territories','Operation_y' : 'Operation'}, inplace = True)
out_mat_unmat_acc_out=pd.concat([out_mat_unmat_acc, out_unmat_terr_match_acc]).drop_duplicates()
out_mat_unmat_acc_out.to_excel('dataoci/Matched_unmatched_accounts_and_unmatched_territories.xlsx',index=False)