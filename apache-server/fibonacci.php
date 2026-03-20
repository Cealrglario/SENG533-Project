<?php
// Function for dynamic loading of the Apache server
function calculateFibonacci($n) {
    if ($n <= 1) {return $n;}
    return calculateFibonacci($n - 1) + calculateFibonacci($n - 2);
}

echo "Fibonacci 35: " . calculateFibonacci(35);
?>