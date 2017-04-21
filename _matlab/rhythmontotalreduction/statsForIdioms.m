function outStruct = statsForIdioms(foldName, filName, inStruct)

tmpF = sprintf('.\\mergedTotalRedMeasures\\%s\\%s', foldName, filName);

fid = fopen(tmpF,'rt');
tmp = textscan(fid,'%s %s','Delimiter',';');
fclose(fid);

outStruct = [];

% dummy initialisation
firstFlag = 1;
lastFlag = 0;


if ~isempty(inStruct)
    outStruct = inStruct;
else
    outStruct.timeSignature = '';
    
    outStruct.firstBarPattern = struct();
    outStruct.firstBarPattern.pattern = [];
    outStruct.firstBarPattern.occurs = [];
    
    outStruct.lastBarPattern = struct();
    outStruct.lastBarPattern.pattern = [];
    outStruct.lastBarPattern.occurs = [];
    
    outStruct.intermPattern = struct();
    outStruct.intermPattern.pattern = [];
    outStruct.intermPattern.occurs = [];
    
end

for i = 1:size(tmp{1,1},1);
    % check if we have a TS indication
    if strcmp(tmp{1,1}{i}, 'TS')
        % check if this time signature is already recorded
        tsFound = 0;
        for j = 1:length(outStruct)
            if strcmp(tmp{1,2}{i}, outStruct(j).timeSignature)
                tsFound = 1;
                tsIDX = j;
                break;
            end
        end
        if ~tsFound
            if strcmp(outStruct(1).timeSignature, '')
                tsIDX = 1;
            else
                tsIDX = length(outStruct) + 1;
            end
            
            outStruct(tsIDX).timeSignature = tmp{1,2}{i};

            outStruct(tsIDX).firstBarPattern = struct();
            outStruct(tsIDX).firstBarPattern.pattern = [];
            outStruct(tsIDX).firstBarPattern.occurs = [];

            outStruct(tsIDX).lastBarPattern = struct();
            outStruct(tsIDX).lastBarPattern.pattern = [];
            outStruct(tsIDX).lastBarPattern.occurs = [];

            outStruct(tsIDX).intermPattern = struct();
            outStruct(tsIDX).intermPattern.pattern = [];
            outStruct(tsIDX).intermPattern.occurs = [];
        end
    end
    if strcmp(tmp{1,1}{i}, 'Grp')
        firstFlag = 1;
    elseif strcmp(tmp{1,1}{i}, 'Bar')
        % check if next is a group or there is no next
        if i+1 > size(tmp{1,1},1)
            lastFlag = 1;
        else
            if strcmp(tmp{1,1}{i+1}, 'Grp')
                lastFlag = 1;
            else
                lastFlag = 0;
            end
        end
        if i <= length(tmp{1,2})
            currBar = str2num(tmp{1,2}{i});
        else
            currBar = [];
        end
        if firstFlag
            % check if we already have that bar in the first bars
            barFound = 0;
            for j = 1:length(outStruct(tsIDX).firstBarPattern)
                if isequal(currBar, outStruct(tsIDX).firstBarPattern(j).pattern)
                    barFound = 1;
                    barIDX = j;
                    
                    outStruct(tsIDX).firstBarPattern(barIDX).pattern = ...
                        currBar;
                    outStruct(tsIDX).firstBarPattern(barIDX).occurs = ...
                        outStruct(tsIDX).firstBarPattern(barIDX).occurs + 1;
                    
                    break;
                end
            end
            if ~barFound
                if isempty(outStruct(tsIDX).firstBarPattern(j).occurs)
                    barIDX = 1;
                else
                    barIDX = length(outStruct(tsIDX).firstBarPattern) + 1;
                end
                
                outStruct(tsIDX).firstBarPattern(barIDX).pattern = ...
                    currBar;
                outStruct(tsIDX).firstBarPattern(barIDX).occurs = 1;
            end
        elseif lastFlag
            % check if we already have that bar in the last bars
            barFound = 0;
            for j = 1:length(outStruct(tsIDX).lastBarPattern)
                if isequal(currBar, outStruct(tsIDX).lastBarPattern(j).pattern)
                    barFound = 1;
                    barIDX = j;
                    
                    outStruct(tsIDX).lastBarPattern(barIDX).pattern = ...
                        currBar;
                    outStruct(tsIDX).lastBarPattern(barIDX).occurs = ...
                        outStruct(tsIDX).lastBarPattern(barIDX).occurs + 1;
                    
                    break;
                end
            end
            if ~barFound
                if isempty(outStruct(tsIDX).lastBarPattern(j).occurs)
                    barIDX = 1;
                else
                    barIDX = length(outStruct(tsIDX).lastBarPattern) + 1;
                end
                
                outStruct(tsIDX).lastBarPattern(barIDX).pattern = ...
                    currBar;
                outStruct(tsIDX).lastBarPattern(barIDX).occurs = 1;
            end
        else
            % check if we already have that bar in the intermediate bars
            barFound = 0;
            for j = 1:length(outStruct(tsIDX).intermPattern)
                if isequal(currBar, outStruct(tsIDX).intermPattern(j).pattern)
                    barFound = 1;
                    barIDX = j;
                    
                    outStruct(tsIDX).intermPattern(barIDX).pattern = ...
                        currBar;
                    outStruct(tsIDX).intermPattern(barIDX).occurs = ...
                        outStruct(tsIDX).intermPattern(barIDX).occurs + 1;
                    
                    break;
                end
            end
            if ~barFound
                if isempty(outStruct(tsIDX).intermPattern(j).occurs)
                    barIDX = 1;
                else
                    barIDX = length(outStruct(tsIDX).intermPattern) + 1;
                end
                
                outStruct(tsIDX).intermPattern(barIDX).pattern = ...
                    currBar;
                outStruct(tsIDX).intermPattern(barIDX).occurs = 1;
            end
        end
        
        firstFlag = 0;
        
    end
end

% for i = 1:size(tmp{3},1)
%     
%     d{i,1} = tmp{1}{i};
%     d{i,2} = tmp{2}(i);
%     d{i,3} = str2num(tmp{3}{i});
%     
% end

% read line by line

% h = {'time','surface','reduction','melodyPC', 'melodyMIDI'};
% 
% tmpKey = 0;
% tmpMode = [0, 2, 4, 5, 7, 9, 11];
% 
% tmpIdx = 2;
% prevTime = -1;
% 
% for i = 1:size(d,1)
%     
%     currTime = d{i,2};
%     
%     if strcmp(d{i,1}, 'tonality')
%         tmpKey = 0;
%         tmpMode = mod(d{i,3} - tmpKey, 12);
%         
%         tmpIdx = tmpIdx + 1;
%         
%         h{tmpIdx, 1} = 'tonality';
%         h{tmpIdx, 2} = '-------';
%         h{tmpIdx, 3} = '-------';
%         h{tmpIdx, 4} = '-------';
%         h{tmpIdx, 5} = '-------';
%     elseif strcmp(d{i,1}, 'grouping')
%         
%         tmpIdx = tmpIdx + 1;
%         
%         h{tmpIdx, 1} = 'grouping';
%         h{tmpIdx, 2} = '-------';
%         h{tmpIdx, 3} = '-------';
%         h{tmpIdx, 4} = '-------';
%         h{tmpIdx, 5} = '-------';
%     else
%         if currTime ~= prevTime
%             prevTime = currTime;
%             tmpIdx = tmpIdx + 1;
%         end
%         h{tmpIdx, 1} = currTime;
%         if strcmp(d{i,1}, 'surface')
%             % h{tmpIdx, 2} = d{i,3};
%             % h{tmpIdx, 4} = max(d{i,3});
%             [r,t,x] = HARM_keyMergeConsRoot(...
%                     d{i,3},...
%                     tmpKey,...
%                     tmpMode);
%             h{tmpIdx, 2} = sprintf('[%d,_',r{1});
%             tmpX = [t{1},x{1}];
%             for j = 1:length(tmpX)
%                 h{tmpIdx, 2} = strcat(h{tmpIdx, 2}, sprintf('%d_',tmpX(j)));
%             end
%             h{tmpIdx, 2} = strcat(h{tmpIdx, 2}, ']');
%             % h{tmpIdx, 4} = mod(max(d{i,3}) - tmpKey, 12);
%         elseif strcmp(d{i,1}, 'reduction')
%             % h{tmpIdx, 3} = d{i,3};
%             [r,t,x] = HARM_keyMergeConsRoot(...
%                     d{i,3},...
%                     tmpKey,...
%                     tmpMode);
%             h{tmpIdx, 3} = sprintf('[%d,_',r{1});
%             tmpX = [t{1},x{1}];
%             for j = 1:length(tmpX)
%                 h{tmpIdx, 3} = strcat(h{tmpIdx, 3}, sprintf('%d_',tmpX(j)));
%             end
%             h{tmpIdx, 3} = strcat(h{tmpIdx, 3}, ']');
%         else
%             h{tmpIdx, 4} = mod(max(d{i,3}) - tmpKey, 12);
%             h{tmpIdx, 5} = max(d{i,3});
%         end
%     end
%     
%     cell2csv(strcat(filName,'.csv'), h, ';');
%     movefile(strcat(filName,'.csv'), sprintf('./output/%s',foldName));
%     
% end