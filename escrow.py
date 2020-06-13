import smartpy as sp

#Both buyer and seller must send in twice the value of the item they are transacting on. This ensures that both parties are committed to see the transaction through to the end. 

class Escrow(sp.Contract):
    def __init__(self):
        self.init(seller = sp.none, buyer = sp.none, price = 0)

    @sp.entry_point
    def setSeller(self, params):
        #ensure seller hasn't already been set
        sp.verify (~self.data.seller.isSome())
        
        #the seller sets the price and must send 2x the price in tez
        self.data.price = params.price
        sp.verify (sp.amount == sp.tez(self.data.price * 2))
        self.data.seller = sp.Some(sp.sender)

    @sp.entry_point
    def setBuyer(self, params):
        #ensure that there already is a seller
        sp.verify (self.data.seller.isSome())
        #ensure buyer hasnt already been set
        sp.verify (~self.data.buyer.isSome())
        
        sp.verify (sp.amount == sp.tez(self.data.price * 2))
        self.data.buyer = sp.Some(sp.sender)
        
    @sp.entry_point
    def confirmReceived(self, params):
        sp.verify (sp.sender == self.data.buyer.openSome())
        sp.send (self.data.buyer.openSome(), sp.tez(self.data.price))
        sp.send (self.data.seller.openSome(), sp.balance)
        self.resetContract()

    @sp.entry_point
    def refundBuyer(self, params):
        sp.verify (sp.sender == self.data.seller.openSome())
        sp.send (self.data.buyer.openSome(), sp.tez(2 * self.data.price))
        sp.send (self.data.seller.openSome(), sp.balance)
        self.resetContract()
        
    #clear out buyer and seller
    def resetContract(self):
        self.data.buyer = sp.none
        self.data.seller = sp.none
        self.data.price = 0

@sp.add_test(name = "Test Escrow")
def testEscrow():
  html = ""
  seller = "AAA"
  buyer = "BBB"

  myContract = Escrow()

  #set the seller and price
  html += myContract.setSeller(price = 1).run(sp.address(seller), amount = sp.tez(2)).html()
  
  #set the buyer
  html += myContract.setBuyer().run(sp.address(buyer), amount = sp.tez(2)).html()
  
  # buyer confirms they received item 
  html += myContract.confirmReceived().run(sp.address("BBB")).html()
  
  # seller decides to refund buyer
  # html += myContract.refundBuyer().run(sp.address(seller)).html()
  
  setOutput(html)
