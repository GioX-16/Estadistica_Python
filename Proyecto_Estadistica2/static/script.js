window.onload = function() {
    const ctx = document.getElementById('scatterChart').getContext('2d');
    const xValues = JSON.parse(ctx.canvas.getAttribute('data-xvalues'));
    const yValues = JSON.parse(ctx.canvas.getAttribute('data-yvalues'));

    const scatterData = xValues.map((x, i) => {
        return { x: x, y: yValues[i] };
    });

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Gráfico de Dispersión',
                data: scatterData,
                backgroundColor: 'rgba(75, 192, 192, 1)'
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Puntaje de Aptitud (X)' }},
                y: { title: { display: true, text: 'Puntaje de Satisfacción (Y)' }}
            }
        }
    });
}
