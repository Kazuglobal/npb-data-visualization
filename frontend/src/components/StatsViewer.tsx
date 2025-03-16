import React, { useState, useEffect } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Select,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Spinner,
  Alert,
  AlertIcon,
  Text,
  useColorModeValue
} from '@chakra-ui/react';

type StatsType = 'batting' | 'pitching' | 'fielding';
type ViewType = 'team' | 'individual' | 'leaders';

interface StatsData {
  [key: string]: any;
}

export default function StatsViewer() {
  const [viewType, setViewType] = useState<ViewType>('team');
  const [statsType, setStatsType] = useState<StatsType>('batting');
  const [data, setData] = useState<StatsData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    fetchStats();
    fetchLastUpdated();
  }, [viewType, statsType]);

  const fetchStats = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/${viewType}/${statsType}`);
      if (!response.ok) {
        throw new Error('Failed to fetch statistics');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchLastUpdated = async () => {
    try {
      const response = await fetch('http://localhost:8000/last_updated');
      if (response.ok) {
        const result = await response.json();
        setLastUpdated(new Date(result.last_updated).toLocaleString());
      }
    } catch (err) {
      console.error('Failed to fetch last updated timestamp:', err);
    }
  };

  const renderTable = () => {
    if (!data.length) return null;

    const headers = Object.keys(data[0]);

    return (
      <Box overflowX="auto">
        <Table variant="simple" size="sm">
          <Thead>
            <Tr>
              {headers.map((header) => (
                <Th key={header}>{header}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {data.map((row, index) => (
              <Tr key={index}>
                {headers.map((header) => (
                  <Td key={`${index}-${header}`}>{row[header]}</Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    );
  };

  const renderLeaders = () => {
    if (!data.length) return null;

    return data.map((category, index) => (
      <Box key={index} mb={6}>
        <Text fontSize="lg" fontWeight="bold" mb={2}>
          {category.category}
        </Text>
        <Table variant="simple" size="sm">
          <Thead>
            <Tr>
              {Object.keys(category.rankings[0]).map((header) => (
                <Th key={header}>{header}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>
            {category.rankings.map((row: any, rowIndex: number) => (
              <Tr key={rowIndex}>
                {Object.values(row).map((value: any, valueIndex: number) => (
                  <Td key={valueIndex}>{value}</Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    ));
  };

  return (
    <Box bg={bgColor} p={4} borderRadius="lg" borderWidth="1px" borderColor={borderColor}>
      <Tabs onChange={(index) => setViewType(['team', 'individual', 'leaders'][index])}>
        <TabList>
          <Tab>チーム成績</Tab>
          <Tab>個人成績</Tab>
          <Tab>リーダーボード</Tab>
        </TabList>

        <Box my={4}>
          <Select
            value={statsType}
            onChange={(e) => setStatsType(e.target.value as StatsType)}
            width="200px"
          >
            <option value="batting">打撃成績</option>
            <option value="pitching">投手成績</option>
            <option value="fielding">守備成績</option>
          </Select>
        </Box>

        {lastUpdated && (
          <Text fontSize="sm" color="gray.500" mb={4}>
            最終更新: {lastUpdated}
          </Text>
        )}

        {isLoading ? (
          <Box textAlign="center" py={4}>
            <Spinner />
          </Box>
        ) : error ? (
          <Alert status="error">
            <AlertIcon />
            {error}
          </Alert>
        ) : (
          <TabPanels>
            <TabPanel>{renderTable()}</TabPanel>
            <TabPanel>{renderTable()}</TabPanel>
            <TabPanel>{renderLeaders()}</TabPanel>
          </TabPanels>
        )}
      </Tabs>
    </Box>
  );
}