% Define the ranges for the input variables
x_temp = 0:0.1:30;
x_humidity = 0:0.1:100;
x_light = 0:0.1:100;

% Define the membership functions for temperature
temp_low = trimf(x_temp, [0 0 15]);
temp_medium = trimf(x_temp, [10 20 30]);
temp_high = trimf(x_temp, [20 30 30]);

% Define the membership functions for humidity
humidity_dry = gaussmf(x_humidity, [10 20]);
humidity_normal = gaussmf(x_humidity, [10 50]);
humidity_humid = gaussmf(x_humidity, [10 80]);

% Define the membership functions for light
light_dim = trapmf(x_light, [0 0 20 40]);
light_moderate = trapmf(x_light, [30 40 60 70]);
light_bright = trapmf(x_light, [60 80 100 100]);

% Plot membership functions for temperature
figure;
subplot(3,1,1);
plot(x_temp, temp_low, 'b', 'LineWidth', 2); hold on;
plot(x_temp, temp_medium, 'g', 'LineWidth', 2);
plot(x_temp, temp_high, 'r', 'LineWidth', 2);
title('Temperature Membership Functions');
xlabel('Temperature (°C)');
ylabel('Membership Degree');
legend('Low', 'Medium', 'High');
grid on;

% Plot membership functions for humidity
subplot(3,1,2);
plot(x_humidity, humidity_dry, 'b', 'LineWidth', 2); hold on;
plot(x_humidity, humidity_normal, 'g', 'LineWidth', 2);
plot(x_humidity, humidity_humid, 'r', 'LineWidth', 2);
title('Humidity Membership Functions');
xlabel('Humidity (%)');
ylabel('Membership Degree');
legend('Dry', 'Normal', 'Humid');
grid on;

% Plot membership functions for light
subplot(3,1,3);
plot(x_light, light_dim, 'b', 'LineWidth', 2); hold on;
plot(x_light, light_moderate, 'g', 'LineWidth', 2);
plot(x_light, light_bright, 'r', 'LineWidth', 2);
title('Light Membership Functions');
xlabel('Light Intensity (Lux)');
ylabel('Membership Degree');
legend('Dim', 'Moderate', 'Bright');
grid on;

% Create a fuzzy inference system
fis = mamfis('Name','AssistiveCareFIS');

% Add input variables and their membership functions
fis = addInput(fis, [0 30], 'Name', 'Temperature');
fis = addMF(fis, 'Temperature', 'trimf', [0 0 15], 'Name', 'Low');
fis = addMF(fis, 'Temperature', 'trimf', [10 20 30], 'Name', 'Medium');
fis = addMF(fis, 'Temperature', 'trimf', [20 30 30], 'Name', 'High');

fis = addInput(fis, [0 100], 'Name', 'Humidity');
fis = addMF(fis, 'Humidity', 'gaussmf', [10 20], 'Name', 'Dry');
fis = addMF(fis, 'Humidity', 'gaussmf', [10 50], 'Name', 'Normal');
fis = addMF(fis, 'Humidity', 'gaussmf', [10 80], 'Name', 'Humid');

fis = addInput(fis, [0 100], 'Name', 'Light');
fis = addMF(fis, 'Light', 'trapmf', [0 0 20 40], 'Name', 'Dim');
fis = addMF(fis, 'Light', 'trapmf', [30 40 60 70], 'Name', 'Moderate');
fis = addMF(fis, 'Light', 'trapmf', [60 80 100 100], 'Name', 'Bright');

% Add output variables and their membership functions
fis = addOutput(fis, [-10 10], 'Name', 'AdjustTemperature');
fis = addMF(fis, 'AdjustTemperature', 'trimf', [-10 -10 0], 'Name', 'Decrease');
fis = addMF(fis, 'AdjustTemperature', 'trimf', [-5 0 5], 'Name', 'NoChange');
fis = addMF(fis, 'AdjustTemperature', 'trimf', [0 10 10], 'Name', 'Increase');

fis = addOutput(fis, [-100 100], 'Name', 'AdjustLight');
fis = addMF(fis, 'AdjustLight', 'trimf', [-100 -100 0], 'Name', 'Decrease');
fis = addMF(fis, 'AdjustLight', 'trimf', [-50 0 50], 'Name', 'NoChange');
fis = addMF(fis, 'AdjustLight', 'trimf', [0 100 100], 'Name', 'Increase');

fis = addOutput(fis, [-50 50], 'Name', 'AdjustHumidity');
fis = addMF(fis, 'AdjustHumidity', 'trimf', [-50 -50 0], 'Name', 'Decrease');
fis = addMF(fis, 'AdjustHumidity', 'trimf', [-25 0 25], 'Name', 'NoChange');
fis = addMF(fis, 'AdjustHumidity', 'trimf', [0 50 50], 'Name', 'Increase');

% Define fuzzy rules
rules = [
    "If Temperature is High and Humidity is Dry then AdjustTemperature is Decrease and AdjustHumidity is Increase"
    "If Temperature is Low and Humidity is Humid then AdjustTemperature is Increase and AdjustHumidity is Decrease"
    "If Light is Dim then AdjustLight is Increase"
    "If Light is Bright then AdjustLight is Decrease"
    "If Temperature is Medium and Humidity is Normal then AdjustTemperature is NoChange and AdjustHumidity is NoChange"
];

fis = addRule(fis, rules);

% Evaluate the FIS for sample inputs
inputValues = [25 30 70];
outputValues = evalfis(fis, inputValues);

% Display the output values
disp('Output values for the given inputs:');
disp(outputValues);

% Plot the system structure
figure;
plotfis(fis);

% Save the FIS structure
writeFIS(fis, 'AssistiveCareFIS');

% To evaluate and visualize the results for a range of inputs:
[TempGrid, HumidityGrid, LightGrid] = ndgrid(0:5:30, 0:20:100, 0:20:100);
inputs = [TempGrid(:), HumidityGrid(:), LightGrid(:)];
outputs = evalfis(fis, inputs);

% Reshape output for plotting
outputTempAdjust = reshape(outputs(:,1), size(TempGrid));
outputLightAdjust = reshape(outputs(:,2), size(TempGrid));
outputHumidityAdjust = reshape(outputs(:,3), size(TempGrid));

% Plotting the output adjustments
figure;
subplot(3,1,1);
surf(0:5:30, 0:20:100, outputTempAdjust(:,:,3));
title('Temperature Adjustment Surface');
xlabel('Temperature (°C)');
ylabel('Humidity (%)');
zlabel('Temperature Adjustment');
grid on;

subplot(3,1,2);
surf(0:5:30, 0:20:100, outputLightAdjust(:,:,3));
title('Light Adjustment Surface');
xlabel('Temperature (°C)');
ylabel('Humidity (%)');
zlabel('Light Adjustment');
grid on;

subplot(3,1,3);
surf(0:5:30, 0:20:100, outputHumidityAdjust(:,:,3));
title('Humidity Adjustment Surface');
xlabel('Temperature (°C)');
ylabel('Humidity (%)');
zlabel('Humidity Adjustment');
grid on;
