from boardcomposer.solver.beam_search import BeamSearchConfig, beam_search


def test_beam_search_keeps_best_states():
    result = beam_search(
        initial=[0],
        expand=lambda value: [value + 1, value + 2],
        score=lambda value: (value,),
        config=BeamSearchConfig(width=2, depth=2),
    )

    assert result == [4, 3]


def test_beam_search_stops_when_no_candidates():
    result = beam_search(
        initial=[0],
        expand=lambda value: [],
        score=lambda value: (value,),
        config=BeamSearchConfig(width=2, depth=3),
    )

    assert result == [0]
