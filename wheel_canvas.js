function drawGraph() {
    const leftMargin = 40;
    const rightMargin = 50;
    const topMargin = 20;
    const bottomMargin = 40;

    const graphWidth = graphCanvas.width - leftMargin - rightMargin;
    const graphHeight = graphCanvas.height - topMargin - bottomMargin;

    // 배경 초기화
    graphCtx.fillStyle = '#fff';
    graphCtx.fillRect(0, 0, graphCanvas.width, graphCanvas.height);

    // 모눈 그리기
    const stepX = 50;
    const stepY = 50;
    graphCtx.strokeStyle = '#ddd';
    graphCtx.lineWidth = 1;

    graphCtx.beginPath();
    // 세로선
    for (let x = leftMargin; x < graphCanvas.width - rightMargin; x += stepX) {
        graphCtx.moveTo(x, topMargin);
        graphCtx.lineTo(x, graphCanvas.height - bottomMargin);
    }
    // 가로선
    for (let y = topMargin; y < graphCanvas.height - bottomMargin; y += stepY) {
        graphCtx.moveTo(leftMargin, y);
        graphCtx.lineTo(graphCanvas.width - rightMargin, y);
    }
    graphCtx.stroke();

    // 축
    graphCtx.strokeStyle = '#000';
    graphCtx.lineWidth = 2;
    graphCtx.beginPath();
    // y축
    graphCtx.moveTo(leftMargin, topMargin);
    graphCtx.lineTo(leftMargin, graphCanvas.height - bottomMargin);
    // x축
    graphCtx.moveTo(leftMargin, graphCanvas.height - bottomMargin);
    graphCtx.lineTo(graphCanvas.width - rightMargin, graphCanvas.height - bottomMargin);
    graphCtx.stroke();

    // 속도-제동력 직선
    const force = eddy_force(currentSpeed);   // 현재 mass 반영
    const maxForce = eddy_force(max_speed);   // mass가 바뀌면 재계산

    const x0 = leftMargin;
    const y0 = graphCanvas.height - bottomMargin; // force=0
    const x1 = leftMargin + graphWidth * (currentSpeed / max_speed);
    const y1 = y0 - graphHeight * (force / maxForce);

    graphCtx.beginPath();
    graphCtx.strokeStyle = 'red';
    graphCtx.lineWidth = 2;
    graphCtx.moveTo(x0, y0);
    graphCtx.lineTo(x1, y1);
    graphCtx.stroke();

    // 레이블
    graphCtx.fillStyle = '#000';
    graphCtx.font = '14px Arial';
    graphCtx.textBaseline = 'middle';
    // x축 레이블
    graphCtx.fillText("속도 (km/h)", graphCanvas.width - rightMargin - 40, graphCanvas.height - bottomMargin / 2);
    // y축 레이블 (세로 방향)
    graphCtx.save();
    graphCtx.translate(leftMargin / 2, topMargin + graphHeight / 2);
    graphCtx.rotate(-Math.PI / 2);
    graphCtx.fillText("제동력 (N)", 0, 0);
    graphCtx.restore();
}
