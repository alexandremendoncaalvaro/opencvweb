export default function createPointerListener(document) {
    // DOM elements
    const $ = document.querySelector.bind(document)
    const $screenshot = $('#screenshot')
    const $marquee = $('#marquee')

    // Temp variables
    let startX = 0
    let startY = 0
    const marqueeRect = {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
    }

    //Prepare
    $marquee.classList.add('hide')
    $screenshot.addEventListener('pointerdown', startDrag)

    function startDrag(ev) {
        window.addEventListener('pointerup', stopDrag)
        $screenshot.addEventListener('pointermove', moveDrag)
        $marquee.classList.remove('hide')

        startX = ev.layerX
        startY = ev.layerY
        const width = 0
        const height = 0

        Object.assign(marqueeRect, {
            startX,
            startY,
            width,
            height
        })
        drawRect($marquee, marqueeRect)
    }

    function stopDrag(ev) {
        window.removeEventListener('pointerup', stopDrag)
        $screenshot.removeEventListener('pointermove', moveDrag)
        if (ev.target === $screenshot && marqueeRect.width && marqueeRect.height) {
            fetch('/mark?x=' + marqueeRect.x + '&y=' + marqueeRect.y + '&h=' + marqueeRect.height + '&w=' + marqueeRect.width)
                .then((response) => {
                    console.log(response.json())
                    $marquee.classList.add('hide')
                })
        }
    }

    function moveDrag(ev) {
        let x = ev.layerX
        let y = ev.layerY
        let width = startX - x
        let height = startY - y
        if (width < 0) {
            width *= -1
            x -= width
        }
        if (height < 0) {
            height *= -1
            y -= height
        }
        Object.assign(marqueeRect, {
            x,
            y,
            width,
            height
        })
        drawRect($marquee, marqueeRect)
    }

    function drawRect(rect, data) {
        const {
            x,
            y,
            width,
            height
        } = data
        rect.setAttributeNS(null, 'width', width)
        rect.setAttributeNS(null, 'height', height)
        rect.setAttributeNS(null, 'x', x)
        rect.setAttributeNS(null, 'y', y)
        return rect
    }
}