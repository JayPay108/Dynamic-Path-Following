
close all;

inFileName = 'MovementTrajectoryData.txt'; % Change to any file name, if left empy the user will be prompted for file name upon execution

% If the file name is empty, prompt the user
if isempty(inFileName)
    inFileName = input('Enter the name of the input file: ', 's');
end

% If the trajectory file does not exist
if(~isfile(inFileName))
    fprintf('%s does not exist\n', inFileName);
    return;
end

% Reading the file in as a two dimensional matrix
inFile = readmatrix(inFileName);
fprintf('%s read successfully\n', inFileName);

% Count the number of characters to be plotted
numOfChars = 1;
while inFile(1, 2) ~= inFile(numOfChars + 1, 2)
    numOfChars = numOfChars + 1;
end

% Setting up graph's appearance
hold on;
set(gcf, 'Position',  [100, 100, 1000, 1000])
title('Movement Trajectory', 'FontSize', 20);
xlabel('X', 'FontSize', 20);
ylabel('Z', 'FontSize', 20);

axis([-100, 100, -100, 100]);
xticks(-100 : 25 : 100);
yticks(-100 : 25 : 100);

plot([-100, 100], [0, 0], '--', 'Color', '#d3d3d3', 'LineWidth', 2);
plot([0, 0], [-100, 100], '--', 'Color', '#d3d3d3', 'LineWidth', 2);


% Plotting graph
fprintf('Plotting graph\n');
for i = 1 : length(inFile)
    % Plotting velocity
    q = quiver(inFile(i,3), inFile(i,4), inFile(i,5), inFile(i,6), 2);
    q.Color = 'green';
    q.ShowArrowHead = 'off';
    
    % Plotting linear
    q = quiver(inFile(i,3), inFile(i,4), inFile(i,7), inFile(i,8));
    q.Color = 'blue';
    q.ShowArrowHead = 'off';
    
    % Plotting orientation
    q = quiver(inFile(i, 3), inFile(i,4), sin(inFile(i,9)), cos(inFile(i,9)));
    q.Color = 'yellow';
    q.ShowArrowHead = 'off';    
end

steerTypes = ["Stop", "Reserved", "Seek", "Flee", "Arrive", "-", "-", "Follow Path"];

% Plotting postion
for i = 1 : numOfChars
    plot(inFile(i, 3), inFile(i, 4), '.r', 'MarkerSize', 40); % Plotting red circle at start of line
    steerType = inFile(i, 10);
    text(inFile(i, 3) + 3, inFile(i, 4) + 1, steerTypes(steerType), 'Color', 'red');   % Writing steering type next to circle
    
    plot(inFile(i:numOfChars:end, 3), inFile(i:numOfChars:end,4), 'Color', 'red', 'LineWidth', 2);
end

% Setting up the legend
L(1) = plot(nan, nan, 'r', 'LineWidth', 3);
L(2) = plot(nan, nan, 'g', 'LineWidth', 3);
L(3) = plot(nan, nan, 'b', 'LineWidth', 3);
L(4) = plot(nan, nan, 'y', 'LineWidth', 3);
legend(L, {'position', 'velocity', 'linear', 'orientation'}, 'location', 'southeast', 'fontSize', 15);

set(gca, 'YDir','reverse'); % Flipping plot about Y axis

hold off; % Showing fully generated plot
saveas(gcf, 'MovementTrajectoryPlot.png'); % Saving plot as png
fprintf('Saved plot as MovementTrajectoryPlot.png\n');

% End of program

    