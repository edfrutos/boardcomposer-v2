from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.constraints_validator import respects_constraints
from boardcomposer.solver.deduplication import deduplicate_solutions
from boardcomposer.solver.evaluation import evaluate
from boardcomposer.solver.generators import generators_by_name
from boardcomposer.solver.strategies import OptimizationStrategy


class CandidatePipeline:
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy,
    ) -> None:
        self.project = project
        self.strategy = strategy

    def run(self) -> list[AssemblySolution]:
        candidates: list[AssemblySolution] = []

        for generator in generators_by_name(list(self.strategy.generator_names)):
            candidates.extend(generator(self.project))

        valid = [
            solution
            for solution in candidates
            if respects_constraints(solution, self.project.constraints)
        ]

        unique = deduplicate_solutions(valid)

        evaluated = [
            evaluate(
                solution,
                total_boards=len(self.project.boards),
                weights=self.strategy.weights,
            )
            for solution in unique
        ]

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )
