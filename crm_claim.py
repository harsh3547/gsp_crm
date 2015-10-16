from openerp.osv import fields ,osv ,orm
#from _smbc import Context

class crm_claim(osv.osv):
    _name="crm.claim"
    _inherit="crm.claim"
    _description="claim module"
    _columns={
              'name':fields.char(string="subject",size=100),
              'user_id':fields.many2one('res.users','responsible'),
              'email_from':fields.char(string="from",size=100),
              }
    
    def create(self,cr,uid,vals,context=None):
          object_send=self.pool.get('mail.mail')
          s=vals.get('name')
          t=vals.get('user_id')
          f=vals.get('email_from')
          object=self.pool.get('res.users').browse(cr,uid,t,context)
          e=object.email
          obj=self.pool.get('mail.compose.message')
          id=obj.create(cr,uid,{},context)
          ir_model_data = self.pool.get('ir.model.data')
          template_id = ir_model_data.get_object_reference(cr, uid, 'gsp_crm', 'email_template_edi_claim')[1]
          claim_id = super(crm_claim,self).create(cr,uid,vals,context)
          values=obj.onchange_template_id(cr,uid,[id],template_id,'comment','crm.claim',claim_id,context)
          value_body=values.get('value').get('body')
          id_create=object_send.create(cr,uid,{'email_from':f,'email_to':e,'subject':s,'body_html':value_body },context)
          object_send.send(cr, uid,[id_create], auto_commit=False, raise_exception=False, context=None)
          return claim_id
        
        
        
                            
                            
                            
                            
        
    
    
    
    
    
   
