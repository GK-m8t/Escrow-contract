import smartpy as sp
#buyer must send in twice the value of the item they are transacting on,while the seller sends in the value of the item. This ensures that both parties are committed to see the transaction through to the end.
class Escrow(sp.Contract):
    def __init__(self):
        self.init(seller = sp.none, buyer = sp.none, price = 0)
    @sp.entry_point
    def setSeller(self, params):
        #ensure seller hasn't already been set
        sp.verify (~self.data.seller.is_some())
        
        #the seller sets the price and must send the price in mutez as insurance
        self.data.price = params.price
        sp.verify (sp.amount == sp.mutez(self.data.price))
        self.data.seller = sp.some(sp.sender)
    @sp.entry_point
    def setBuyer(self):
        #ensure that there already is a seller
        sp.verify (self.data.seller.is_some())
        #ensure buyer hasnt already been set
        sp.verify (~self.data.buyer.is_some())
        
        sp.verify (sp.amount == sp.mutez(self.data.price * 2))
        self.data.buyer = sp.some(sp.sender)
        
    @sp.entry_point
    def confirmReceived(self):
        sp.verify (sp.sender == self.data.buyer.open_some())
        sp.send (self.data.buyer.open_some(), sp.mutez(self.data.price))
        sp.send (self.data.seller.open_some(), sp.mutez(3 * self.data.price))
        self.resetContract()
    @sp.entry_point
    def refundBuyer(self):
        sp.verify (sp.sender == self.data.seller.open_some())
        sp.send (self.data.buyer.open_some(), sp.mutez(2 * self.data.price))
        sp.send (self.data.seller.open_some(), sp.mutez(2 * self.data.price))
        self.resetContract()
        
    #clear out buyer and seller
    def resetContract(self):
        self.data.buyer = sp.none
        self.data.seller = sp.none
        self.data.price = 0
        
@sp.add_test(name = "Test Escrow")
def testEscrow():
    html = sp.test_scenario()
    
    html.h1("Escrow Cont")
    seller = sp.test_account("seller")
    buyer = sp.test_account("buyer")
    
    myContract = Escrow()
     #set the seller and price
    html += myContract
    
    html += myContract.setSeller(price = 1).run(sender = seller, amount = sp.mutez(1))
     #set the buyer
    html += myContract.setBuyer().run(sender = buyer, amount = sp.mutez(2))
    # buyer confirms they received item 
    html += myContract.confirmReceived().run(sender = buyer)
  
     # seller decides to refund buyer
     # html += myContract.refundBuyer().run(sp.address(seller)).html()
