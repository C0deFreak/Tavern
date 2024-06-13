import React, {useState, useEffect} from "react"
import api from './api'

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    is_income: false,
    date: ''
  });

  const fetchTransactions = async () => {
    const response = await api.get('transactions/');
    setTransactions(response.data)
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/transactions/', formData);
    fetchTransactions();
    setFormData({
      amount: '',
      category: '',
      description: '',
      is_income: false,
      date: ''
    });
  };

  return (
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Finance App
          </a>
        </div>
      </nav>

      <div className="container">
        <form onSubmit={handleFormSubmit}>

          <div className="mb-3 mt-3">
            <lable htmlFor='amount' className='form-lable'>
              Amount
            </lable>
            <input type="text" className="form-control" id="amount" name="amount" onChange={handleInputChange} value={formData.amount}/>
          </div>

          <div className="mb-3">
            <lable htmlFor='category' className='form-lable'>
              Category
            </lable>
            <input type="text" className="form-control" id="category" name="category" onChange={handleInputChange} value={formData.category}/>
          </div>

          <div className="mb-3">
            <lable htmlFor='description' className='form-lable'>
              Description
            </lable>
            <input type="text" className="form-control" id="description" name="description" onChange={handleInputChange} value={formData.description}/>
          </div>

          <div className="mb-3">
            <lable htmlFor='is_income' className='form-lable'>
              Income?
            </lable>
            <input type="checkbox" id="is_income" name="is_income" onChange={handleInputChange} value={formData.is_income}/>
          </div>

          <div className="mb-3">
            <lable htmlFor='date' className='form-lable'>
              Date
            </lable>
            <input type="text" className="form-control" id="date" name="date" onChange={handleInputChange} value={formData.date}/>
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>

        </form>

        <table className="table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>Amount</th>
              <th>Category</th>
              <th>Description</th>
              <th>Income?</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>{transaction.amount}</td>
                <td>{transaction.category}</td>
                <td>{transaction.description}</td>
                <td>{transaction.is_income ? 'Yes' : 'No'}</td>
                <td>{transaction.date}</td>
              </tr>
            ))}
          </tbody>
        </table>

      </div>

    </div>
  )
}

export default App;
