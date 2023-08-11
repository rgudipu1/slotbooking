import unittest
from unittest.mock import patch
from io import StringIO
from client import book_my_slot_client

class TestBookMySlotClient(unittest.TestCase):

    @patch('builtins.input')
    @patch('socket.socket')
    def test_successful_slot_booking(self, mock_socket, mock_input):
        self.maxDiff = None 
        mock_conn = mock_socket.return_value
        mock_input.side_effect = ['b001', '1234', '1', '1', '4']
        
        f_output = StringIO()
        with patch('sys.stdout', f_output):
            book_my_slot_client('192.168.1.25', 5678)  
        
        #ep1 is to check server connection
        #ep2 is to check login details are correct or not
        #ep3 displaying main menu after login
        #ep4 display slots
        #ep5 book slots
        #ep6 displaying main menu again
        expected_output1 =('Connected to the BookMySlot server\n')
        expected_output2 =('Successfully logged in to the appointment scheduler.\n')
        expected_output3=('Main Menu\n1. Book a slot for demo\n2. Drop existing slot\n3. view your slot details\n4. Exit\n\n\n\n')
        expected_output4=('book your slot\n1.10MAY,9:00-9:20\n2.10MAY,3:00-3:20\n3.10MAY,3:20-3:40\n4.10MAY,4:00-4:20\n5.11MAY,9:20-9:40\n6.11MAY,1:00-1:20\n7.11MAY,1:20-1:40\n8.11MAY,3:20-3:40\n9.11MAY,4:00-4:20\n\n')
        expected_output5=('Slot booked successfully\n\n')
        expected_output6=('Main Menu\n1. Book a slot for demo\n2. Drop existing slot\n3. view your slot details\n4. Exit\n\n\n')
        total_output=expected_output1+expected_output2+expected_output3+expected_output4+expected_output5+expected_output6
        m=f_output.getvalue()
        self.assertEqual(m,total_output)
    
    @patch('builtins.input')
    @patch('socket.socket')
    def test_unsuccessful_slot_booking(self, mock_socket, mock_input):
        self.maxDiff = None 
        mock_conn = mock_socket.return_value
        mock_input.side_effect = ['b001', '1234', '1', '4']
        
        f_output = StringIO()
        with patch('sys.stdout', f_output):
            book_my_slot_client('192.168.1.25', 5678)  
        expected_output1 =('Connected to the BookMySlot server\n')
        expected_output2 =('Successfully logged in to the appointment scheduler.\n')
        expected_output3=('Main Menu\n1. Book a slot for demo\n2. Drop existing slot\n3. view your slot details\n4. Exit\n\n\n\n')
        expected_output4=('Your slot is already booked.\nPlease use drop option to drop your existing slot\n\n')
        expected_output5=('Main Menu\n1. Book a slot for demo\n2. Drop existing slot\n3. view your slot details\n4. Exit\n\n\n')
        total_output=expected_output1+expected_output2+expected_output3+expected_output4+expected_output5
        m=f_output.getvalue()
        self.assertEqual(m,total_output)
        
if __name__ == '__main__':
    unittest.main()
