require 'rails_helper'

describe Reconciler do
  let(:bank_transaction) { create :bank_transaction, amount: total }
  let(:current_admin) { create :admin }
  let(:wells_fargo_account) { Account.wells_fargo_cash }

  subject { described_class.new bank_transaction, wells_fargo_account.id, reconciliations, current_admin }

  describe "#reconcile!" do
    let(:reconciliations) {{
        customer1_account_id => amount1,
        customer2_account_id => amount2
    }}

    context "a deposit" do
      let(:amount1) { 123 }
      let(:amount2) { 300 }
      let(:total)   { amount1 + amount2 }
      let(:customer1_account_id) { create(:lender_with_accounts).cash_account.id }
      let(:customer2_account_id) { create(:lender_with_accounts).cash_account.id }

      it "reconciles the transaction" do
        subject.reconcile!
        expect(Transaction.where credit_id: customer1_account_id,
                                 debit_id: wells_fargo_account.id,
                                 amount: amount1).to exist
        expect(Transaction.where credit_id: customer2_account_id,
                                 debit_id: wells_fargo_account.id,
                                 amount: amount2).to exist
      end

      it "returns true" do
        expect(subject.reconcile!).to be true
      end
    end

    context "a withdrawal" do
      let(:amount1) { -123 }
      let(:amount2) { -300 }
      let(:total)   { amount1 + amount2 }
      let(:customer1_account_id) { create(:borrower_with_accounts).loan_account.id }
      let(:customer2_account_id) { create(:borrower_with_accounts).loan_account.id }

      before do
        # put enough money in the Wells Fargo account beforehand
        create(:transaction, credit_id: create(:lender_cash_account).id,
                             debit_id: wells_fargo_account.id,
                             amount: 1000)
        subject.reconcile!
      end

      it "reconciles the transaction" do
        expect(Transaction.where credit_id: wells_fargo_account.id,
                                 debit_id: customer1_account_id,
                                 amount: -amount1).to exist
        expect(Transaction.where credit_id: wells_fargo_account.id,
                                 debit_id: customer2_account_id,
                                 amount: -amount2).to exist
      end
    end

    context "with an invalid account id" do
      let(:amount1) { 123 }
      let(:amount2) { 300 }
      let(:total)   { amount1 + amount2 }
      let(:customer1_account_id) { 123456789 }
      let(:customer2_account_id) { 987654321 }


      it "throws an error" do
        expect{subject.reconcile!}.to raise_error ActiveRecord::InvalidForeignKey
      end
    end

    context "with insufficient funds in one of the accounts" do
      let(:other_account_id) { create(:lender_with_accounts).cash_account.id }
      let(:total) { -123 }
      let(:reconciliations) { {other_account_id => total} }

      it "throws an error" do
        expect{subject.reconcile!}.to raise_error ActiveRecord::StatementInvalid do |error|
          expect(error.original_exception).to be_a PG::CheckViolation
        end
      end
    end
  end

  describe "#reconcile" do
    context "with insufficient funds in one of the accounts" do
      let(:other_account_id) { create(:lender_with_accounts).cash_account.id }
      let(:total) { -123 }
      let(:reconciliations) { {other_account_id => total} }

      it "does not reconcile the transaction" do
        expect(subject.reconcile).to be false
      end
    end
  end
end
